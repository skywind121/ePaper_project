#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

#GPIO library
import RPi.GPIO as GPIO
import time
#GPIO setting
GPIO.setmode(GPIO.BCM)
BTN_PIN = 26
WAIT_TIME = 0.2
GPIO.setup(BTN_PIN, GPIO.IN)
previousStatus = None
previousTime = time.time()
currentTime  = None

#ePaper library
import logging
from waveshare_epd import epd7in5_V2
from PIL import Image,ImageDraw,ImageFont
import traceback

from futureWeather import * #input weather information 
from data import *  #input the googlesheet data
from datetime import datetime   #get the date

logging.basicConfig(level=logging.DEBUG)

#clean ePaper 
def clearPaper():
    logging.info("Clear...")
    epd.init()
    epd.Clear()

#show page 1    
def page1():
    Himage2 = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    bmp = Image.open(os.path.join(picdir, 'page1.bmp'))
    bmp = bmp.resize((799,479),Image.BILINEAR)    
    Himage2.paste(bmp, (1,1))
    mail = Image.open(os.path.join(picdir, 'mail.bmp'))
    mail = mail.resize((80,60),Image.BILINEAR)    
    Himage2.paste(mail, (584,18))
    
    qrcode = Image.open(os.path.join(picdir, 'qrcode.bmp'))
    qrcode = qrcode.resize((110,110),Image.BILINEAR)    
    Himage2.paste(qrcode, (689,2))
    
    
    draw = ImageDraw.Draw(Himage2)    
    draw.text((10, 120), jobPosition, font = font75, fill = 0)
    draw.text((170, 175), showName, font = font90, fill = 0)
    draw.text((470, 210), nowStatus, font = font60, fill = 0)
    draw.text((608, 78), '99+', font = font24, fill = 0)
    
    draw.text((20, 40), datetime.today().strftime('%Y') + '年', font = font30, fill = 0)
    draw.text((125, 40), datetime.today().strftime('%m') + '月', font = font30, fill = 0)
    draw.text((200, 40), datetime.today().strftime('%d') + '日', font = font30, fill = 0)
    
    draw.text((300, 25), keelungName, font = font30, fill = 0)
    draw.text((420, 25), futureTemp[0] + '°', font = font30, fill = 0)    
    draw.text((480, 25), futureHumi[0] + '%', font = font30, fill = 0)
    draw.text((300, 60), futureWea[0], font = font30, fill = 0)
    
    epd.display(epd.getbuffer(Himage2))    

#show page 2    
def page2():
    Himage2 = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    
    bmp = Image.open(os.path.join(picdir, 'page2.bmp'))
    bmp = bmp.resize((799,479),Image.BILINEAR)    
    Himage2.paste(bmp, (1,1))    
    
    draw = ImageDraw.Draw(Himage2)
    draw.text((20, 20), '未來一週天氣預報', font = font60, fill = 0)
    draw.text((660, 35), keelungName, font = font45, fill = 0)    
    draw.text((20, 120), '今天', font = font30, fill = 0)
    draw.text((148, 120), '明天', font = font30, fill = 0)
    draw.text((258, 120), '後天', font = font30, fill = 0)
    draw.text((20, 160), futureDate[0], font = font24, fill = 0)
    draw.text((20, 200), '溫度', font = font30, fill = 0)
    draw.text((20, 235), futureTemp[0] + '°C' , font = font24, fill = 0)
    draw.text((20, 280), '濕度', font = font30, fill = 0)
    draw.text((20, 315), futureHumi[0] + '%' , font = font24, fill = 0)
    draw.text((20, 360), '天氣', font = font30, fill = 0)
    if len(futureWea[0]) > 4 :
        draw.text((20, 400), (futureWea[0])[0:4], font = font20, fill = 0)
        draw.text((20, 430), (futureWea[0])[5:], font = font20, fill = 0)
    else:
        draw.text((20, 400), futureWea[0], font = font20, fill = 0)
    
    x = 148
    for i in range(1,7):
        draw.text((x, 160), futureDate[i], font = font24, fill = 0)
        draw.text((x, 200), '溫度', font = font30, fill = 0)
        draw.text((x, 235), futureTemp[i] + '°C' , font = font24, fill = 0)
        draw.text((x, 280), '濕度', font = font30, fill = 0)
        draw.text((x, 315), futureHumi[i] + '%' , font = font24, fill = 0)
        draw.text((x, 360), '天氣', font = font30, fill = 0)
        if len(futureWea[i]) > 4 :
            draw.text((x, 400), (futureWea[i])[0:4], font = font20, fill = 0)
            draw.text((x, 430), (futureWea[i])[4:], font = font20, fill = 0)
        else:
            draw.text((x, 400), futureWea[i], font = font20, fill = 0)
        x = x + 110
    
    epd.display(epd.getbuffer(Himage2))

#show page 3
def page3():
    Himage2 = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    
    bmp = Image.open(os.path.join(picdir, 'page3.bmp'))
    bmp = bmp.resize((799,479),Image.BILINEAR)    
    Himage2.paste(bmp, (1,1))    
    
    draw = ImageDraw.Draw(Himage2)
    draw.text((45, 33), '留言板', font = font45, fill = 0)
    messX = 145
    for i in range(0,5):
        draw.text((20, messX), no[i], font = font24, fill = 0)
        draw.text((160, messX), name[i], font = font24, fill = 0)
        draw.text((270, messX), mess[i], font = font24, fill = 0)
        messX = messX + 70
        
    epd.display(epd.getbuffer(Himage2))      
    
try:
    logging.info("epd7in5_V2 Demo")
    epd = epd7in5_V2.EPD()    
    clearPaper()
    
    #front setting
    font90 = ImageFont.truetype(os.path.join(picdir, 'Font3.ttc'), 90)
    font75 = ImageFont.truetype(os.path.join(picdir, 'Font3.ttc'), 75)
    font60 = ImageFont.truetype(os.path.join(picdir, 'Font3.ttc'), 60)
    font45 = ImageFont.truetype(os.path.join(picdir, 'Font3.ttc'), 45)
    font30 = ImageFont.truetype(os.path.join(picdir, 'Font3.ttc'), 30)
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font2.ttc'), 24)
    font20 = ImageFont.truetype(os.path.join(picdir, 'Font2.ttc'), 20)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font3.ttc'), 18)   
    
    page1()        
    page = 2
    while True:
        input = GPIO.input(BTN_PIN)
        currentTime = time.time()
        
        #button change page
        if input == GPIO.LOW and previousStatus == GPIO.HIGH and (currentTime - previousTime) > WAIT_TIME:
            previousTime = currentTime
            if page == 4:
                page = 1
            if page == 1:
                page1()
            elif page == 2:
                page2()
            elif page == 3:
                page3()
            page = page + 1
        previousStatus = input
    
    '''clearPaper()   
    logging.info("Goto Sleep...")
    epd.sleep()'''
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    print("Exception: KeyboardInterrupt")
    epd7in5_V2.epdconfig.module_exit()
    exit()
    
finally:
    GPIO.cleanup()    
