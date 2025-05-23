import RPi.GPIO as GPIO
import time
import subprocess
import boto3
import os
import sounddevice as sd
import soundfile as sf
import numpy as np
import queue
from datetime import datetime
import uuid

LEVER_PIN = 17
UPLOAD_DIR = "uploads"
GREETING_FILE = "Greeting.wav"
BEEP_FILE = "Beep.wav"
BUCKET_NAME = "kayla-audio-guestbook"

os.makedirs(UPLOAD_DIR, exist_ok=True)

# GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(LEVER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# S3 
s3 = boto3.client('s3')

# Audio parameters (recording)
samplerate = 44100
channels = 1
dtype = 'int16'
audio_q = queue.Queue()

def audio_callback(indata, frames, time_info, status):
    if status:
        print(f"Recording status: {status}")
    audio_q.put(indata.copy())

print("Waiting for phone to be picked up...")

try:
    while True:
        if GPIO.input(LEVER_PIN) == GPIO.LOW:
            print("Phone picked up - playing greeting.")
            subprocess.run(["aplay", GREETING_FILE])

            print("Playing beep.")
            subprocess.run(["aplay", BEEP_FILE])

            print("Recording started...")
            with sd.InputStream(samplerate=samplerate, channels=channels, dtype=dtype, callback=audio_callback):
                while GPIO.input(LEVER_PIN) == GPIO.LOW:
                    time.sleep(0.1)

            print("Phone hung up. Stopping recording...")

            # Collect audio from queue
            recorded_audio = []
            while not audio_q.empty():
                recorded_audio.append(audio_q.get())
            full_audio = np.concatenate(recorded_audio, axis=0)

            # Save to file with datestamp locally
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"guest_message_{timestamp}_{uuid.uuid4().hex[:6]}.wav"
            filepath = os.path.join(UPLOAD_DIR, filename)
            sf.write(filepath, full_audio, samplerate)
            print(f"Recording saved to {filepath}")

            # Upload audio to S3
            try:
                s3.upload_file(filepath, BUCKET_NAME, filename)
                print(f"Uploaded {filename} to S3 bucket {BUCKET_NAME}")
            except Exception as e:
                print(f"Upload failed: {e}")

            time.sleep(1)  # debounce
        else:
            print("Phone is on the hook.")
        time.sleep(0.5)

except KeyboardInterrupt:
    GPIO.cleanup()
