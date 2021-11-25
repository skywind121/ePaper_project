import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
BTN_PIN = 37
WAIT_TIME = 0.2
GPIO.setup(BTN_PIN, GPIO.IN)
previousStatus = None
previousTime = time.time()
currentTime  = None

try:
    page = 0
    while True:
        input = GPIO.input(BTN_PIN)
        currentTime = time.time()
        
        if input == GPIO.LOW and previousStatus == GPIO.HIGH and (currentTime - previousTime) > WAIT_TIME:
            previousTime = currentTime
            page = page + 1
            if page == 4:
                page = 1
            print('Page:' + str(page))
        previousStatus = input

except KeyboardInterrupt:
    print("Exception: KeyboardInterrupt")

finally:
    GPIO.cleanup()          
