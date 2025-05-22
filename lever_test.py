import RPi.GPIO as GPIO
import time

# Use BCM numbering
GPIO.setmode(GPIO.BCM)

# Set up GPIO17 as input with internal pull-up resistor
GPIO_PIN = 17
GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Monitoring phone lever switch. Press Ctrl+C to stop.")

try:
    while True:
        if GPIO.input(GPIO_PIN) == GPIO.LOW:
            print("Phone answered")
        else:
            print("Phone hung up")
        time.sleep(0.5)  # prevent spamming output
except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()
