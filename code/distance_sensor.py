import RPi.GPIO as GPIO
import time
from song import playSong

GPIO.setmode(GPIO.BCM) #使用的編碼函式庫
TRIGGER_PIN = 21
ECHO_PIN = 20
GPIO.setup(TRIGGER_PIN, GPIO.OUT) #將trigger(Pin 23)設置為輸出
GPIO.setup(ECHO_PIN, GPIO.IN) #將ECHO(Pin 24)設置為輸入
GPIO.output(TRIGGER_PIN, GPIO.LOW) #trigger(Pin 23)輸出低電位
v = 343 # (331+0.6*25) # 331+0.6T

def measure():
    GPIO.output(TRIGGER_PIN, GPIO.HIGH) #trigger(Pin 23)輸出高電位
    time.sleep(0.00001) #觸發10uS的波來啟動distance sensor(trigger 維持的時間)
    GPIO.output(TRIGGER_PIN, GPIO.LOW)
    pulse_start = None
    pulse_end = None

    while GPIO.input(ECHO_PIN) == GPIO.LOW: 
        pulse_start = time.time() # 記錄低電位的最後時間點
    
    while GPIO.input(ECHO_PIN) == GPIO.HIGH: 
        pulse_end = time.time() # 記錄高電位的最後時間點
    
    t = pulse_end - pulse_start # 物體來回的時間
    d = t * v # 換算來回之距離
    d = d / 2 # 單向距離
    return d * 100 # 轉為公分

def measure_average() : # 多測量幾次來提高準確度
    d1 = measure() # 第一次測量
    time.sleep(0.05)
    d2 = measure() # 第二次測量
    time.sleep(0.05)
    d3 = measure() # 第三次測量
    distance = (d1 + d2 + d3) / 3
    return distance

def check_distance():
    while True:
        distance = measure_average()
        print ("Distance: %.1f (cm)" % distance)
        if(distance < 30):
            playSong()
        time.sleep(1)

check_distance()
