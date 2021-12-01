import RPi.GPIO as GPIO # 載入樹莓派GPIO專用函式庫
import time

GPIO.setmode(GPIO.BCM) # 設定GPIO使用的腳位編號為BCM編號
RED_PIN = 5
YELLOW_PIN = 6
GREEN_PIN = 13

# 將腳位設為輸出腳位，預設值為LOW
GPIO.setup(RED_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(YELLOW_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(GREEN_PIN, GPIO.OUT, initial=GPIO.LOW)

# 副程式，亮暗控制
def TrafficLight(Pin, duration):
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(pin, GPIO.LOW)

# 紅綠燈，持續時間
try:
    while True:
        TrafficLight(RED_PIN, 4);
        TrafficLight(YELLOW_PIN, 2);
        TrafficLight(GREEN_PIN, 4);

# 終止程式，當按下Crtl + C 的動作
except KeyboardInterrupt:
    print ("Exception: KeyboardInterrupt")

finally:
    GPIO.cleanup()
