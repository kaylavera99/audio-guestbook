# wav_playback_test.py
import RPi.GPIO as GPIO
import time
import simpleaudio as sa

LEVER_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(LEVER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Waiting for phone to be picked up...")

try:
    while True:
        if GPIO.input(LEVER_PIN) == GPIO.LOW:
            print("Phone picked up - playing greeting.")
            wave_obj = sa.WaveObject.from_wave_file("Greeting.wav")
            play_obj = wave_obj.play()
            play_obj.wait_done()  # Wait for playback to finish
            print("Playing beep")
            wav_obj2 = sa.WaveObject.from_wave_file("Beep.wav")
            play_obj2 = wav_obj2.play()
            play_obj2.wait_done()
            time.sleep(1)  # Debounce delay
        else:
            print("Phone is on the hook.")
        time.sleep(0.5)
except KeyboardInterrupt:
    GPIO.cleanup()
