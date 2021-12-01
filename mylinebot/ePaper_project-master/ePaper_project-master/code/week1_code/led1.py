import RPi.GPIO as GPIO # 載入樹莓派GPIO專用函式庫
import time

GPIO.setmode(GPIO.BCM) # 設定GPIO使用的腳位編號為BCM編號
LED_PIN = 4 # 將編號4腳位設為連接LED的對應接腳
GPIO.setup(LED_PIN, GPIO.OUT) # 將腳位設為輸出腳位


print ("LED is on")
GPIO.output(LED_PIN, GPIO.HIGH) # 高電位輸出
time.sleep(3)

# 清除GPIO設定 結束程式
GPIO.cleanup

