# test_gpio_input.py
import RPi.GPIO as GPIO
import time

BUTTON_PIN = 17  # GPIO17 (physical pin 11)

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            print("Detected connection (LOW)")
        else:
            print("No connection (HIGH)")
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
