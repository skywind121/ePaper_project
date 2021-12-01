import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM) # 設為BCM mode

R_pin = 13 # R: BOARD:33
G_pin = 19 # G: BOARD:35
B_pin = 26 # B: BOARD:37

GPIO.setup(R_pin, GPIO.OUT) # 將PIN腳位設為輸出
GPIO.setup(G_pin, GPIO.OUT)
GPIO.setup(B_pin, GPIO.OUT)

R_pwm = GPIO.PWM(R_pin, 800) # 設置一個PWM腳位
G_pwm = GPIO.PWM(G_pin, 800)
B_pwm = GPIO.PWM(B_pin, 800)
# use python RPi.GPIO, square wave is 70k Hz
# use python wiringpi2 or bindings, square wave is 28k Hz
# use C wiringPi, square wave is 4.1-4.6M Hz

def check_RGB_range(R,G,B): # 調整色階在合理範圍
    if R < 0 : R = 0
    if G < 0 : G = 0
    if B < 0 : B = 0
    if R > 255 : R = 255
    if G > 255 : G = 255
    if B > 255 : B = 255
    return R,G,B

R,G,B = 255,255,255
state = 0
interval = 8

R_pwm.start(0) # 啟動PWM
G_pwm.start(0)
B_pwm.start(0)

try:
    while(1):
        if (state == 0):
            R = R
            G = G - interval
            B = B - interval
        if (state == 1):
            R = R
            G = G + interval
            B = B
        if (state == 2):
            R = R - interval
            G = G
            B = B
        if (state == 3):
            R = R
            G = G
            B = B + interval
        if (state == 4):
            R = R
            G = G - interval
            B = B
        if (state == 5):
            R = R + interval
            G = G
            B = B
        if (state == 6):
            R = R 
            G = G + interval
            B = B
            
        R,G,B = check_RGB_range(R,G,B) # 檢查色階有沒有超範圍

        if(R == 255 and G == 255 and B == 255): state = 0 # 根據當前RGB値決定狀態
        if(R == 255 and G == 0 and B == 0): state = 1
        if(R == 255 and G == 255 and B == 0): state = 2
        if(R == 0 and G == 255 and B == 0): state = 3
        if(R == 0 and G == 255 and B == 255): state = 4
        if(R == 0 and G == 0 and B == 255): state = 5
        if(R == 255 and G == 0 and B == 255): state = 6
        
        #mapping
        R_mapping = int (R / 255 * 100) # dc為百分比(0-100)，故須將256種色階對映成0-100
        G_mapping = int (G / 255 * 100)
        B_mapping = int (B / 255 * 100)
        
        R_pwm.ChangeDutyCycle(R_mapping) # 設置對映成duty cycle的値
        G_pwm.ChangeDutyCycle(G_mapping)
        B_pwm.ChangeDutyCycle(B_mapping)
        
        print("R,G,B:\t",R,G,B,"\t mapping: ",R_mapping,G_mapping,B_mapping)
        time.sleep(0.3)
        
except Exception as e:
    print(e)
    
finally:
    GPIO.cleanup()
