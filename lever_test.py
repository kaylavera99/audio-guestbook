import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Starting lever test. Press Ctrl+C to stop.")

try:
    while True:
        if GPIO.input(17) == GPIO.LOW:
            print("Phone picked up (HIGH)")
        else:
            print("Phone hung up (LOW)")
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
