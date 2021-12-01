# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 14:04:19 2021

@author: JIMMY
"""

import time
import RPi.GPIO as GPIO

LED_PIN = 26                            # BOARD mode:39
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)           # 將腳位設為輸出

pwm_led = GPIO.PWM(LED_PIN, 100)        # frequency = 100Hz
pwm_led.start(0)                        # 開始亮

try:
    while True:
        for dc in range(0, 101, 5):     # 增加(dc)duty cycle值 
            pwm_led.ChangeDutyCycle(dc) # 設定 duty cycle
            time.sleep(0.1)             # 每0.1秒變化一次
        time.sleep(0.5)

        for dc in range(100, -1, -5):   # 減少duty cycle值
            pwm_led.ChangeDutyCycle(dc)
            time.sleep(0.1)
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Exception: KeyboardInterrupt")

finally:
    pwm_led.stop()                      # 結束時關閉LED脈衝輸出
    GPIO.cleanup()                      # 清除所有GPIO設定

