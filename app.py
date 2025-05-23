import RPi.GPIO as GPIO
import time
import simpleaudio as sa
import sounddevice as sd
import soundfile as sf
import os
import boto3
import uuid
from datetime import datetime

# --- Setup ---
LEVER_PIN = 17
UPLOAD_FOLDER = "uploads"
BUCKET_NAME = "kayla-audio-guestbook"  # ← Replace this with your actual S3 bucket name

GPIO.setmode(GPIO.BCM)
GPIO.setup(LEVER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

s3 = boto3.client('s3')

print("Waiting for phone to be picked up...")

def record_audio(filename, duration=10, fs=44100):
    print("Recording started...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    sf.write(filename, audio, fs)
    print("Recording finished.")

def upload_to_s3(filename):
    try:
        s3.upload_file(filename, BUCKET_NAME, os.path.basename(filename))
        print(f"Uploaded {filename} to S3.")
    except Exception as e:
        print(f"Upload failed: {e}")

try:
    while True:
        if GPIO.input(LEVER_PIN) == GPIO.LOW:
            print("Phone picked up - playing greeting.")
            wave_obj = sa.WaveObject.from_wave_file("Greeting.wav")
            play_obj = wave_obj.play()
            play_obj.wait_done()

            print("Playing beep")
            beep_obj = sa.WaveObject.from_wave_file("Beep.wav")
            play_obj2 = beep_obj.play()
            play_obj2.wait_done()

            time.sleep(1)

            # Start recording
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            unique_id = uuid.uuid4().hex[:6]
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
            filename = f"{UPLOAD_FOLDER}/guest_message_{timestamp}_{unique_id}.wav"
            record_audio(filename)
            upload_to_s3(filename)

            # Wait until phone is hung up
            print("Waiting for phone to hang up...")
            while GPIO.input(LEVER_PIN) == GPIO.LOW:
                time.sleep(0.5)

        else:
            print("Phone is on the hook.")
            time.sleep(0.5)

except KeyboardInterrupt:
    GPIO.cleanup()
    print("Exiting gracefully.")
