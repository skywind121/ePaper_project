import RPi.GPIO as gpio
import time
piano = list([330, 262, 196, 262, 294, 392 ,1,1, 294, 330, 294, 196, 262])
buzzer = 16
gpio.setmode(gpio.BCM)
gpio.setup(buzzer, gpio.OUT)

def play(pitch, sec):
    half_pitch = (1 / pitch) / 4
    t = int(pitch * sec)
    for i in range(t):
        gpio.output(buzzer, gpio.HIGH)
        time.sleep(half_pitch)
        gpio.output(buzzer, gpio.LOW)
        time.sleep(half_pitch)
def playSong():        
    for p in piano:
        play(p, 1)

#playSong()

