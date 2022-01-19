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

import json 
jDataName = 'jsonData.json'
with open(jDataName, 'r') as file_object:
    jData=json.load(file_object)
LineDataName = '/home/pi/ePaper_project/mylinebot/ePaperLineBot/lineData.json'
with open(LineDataName, 'r') as line_object:
    LineData=json.load(line_object)
    
global sName
sName = jData["ShowName"]
global sJobPosition
sJobPosition = jData["JobPosition"]
global sStatus
sStatus = jData["Status"]
global sEmail
sEmail = jData["email"]
global sNewMess 
sNewMess = jData["newMessageNum"]

#clean ePaper 
def clearPaper():
    logging.info("Clear...")
    epd.init()
    epd.Clear()
    
def showWeaIcon(HimageCopy,iconNum, x, y):
    if((iconNum == '02') or (iconNum == '03')):
        weaIcon = Image.open(os.path.join(picdir, 'sunCloud.bmp'))
    elif(iconNum == '04'):
        weaIcon = Image.open(os.path.join(picdir, 'manyCloud.bmp'))
    elif((iconNum == '05') or (iconNum == '06')):
        weaIcon = Image.open(os.path.join(picdir, 'moonCloud.bmp'))
    elif(iconNum == '07'):
        weaIcon = Image.open(os.path.join(picdir, 'moon.bmp'))
    elif((iconNum == '08') or (iconNum == '09') or (iconNum == '10') or (iconNum == '11')):
        weaIcon = Image.open(os.path.join(picdir, 'cloudRain.bmp'))
    else:
        weaIcon = Image.open(os.path.join(picdir, 'cloud.bmp'))
    weaIcon = weaIcon.resize((60,60),Image.BILINEAR)    
    HimageCopy.paste(weaIcon, (x,y))
    

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
    
    ntou = Image.open(os.path.join(picdir, 'ntou.bmp'))
    ntou = ntou.resize((150,150),Image.BILINEAR)    
    Himage2.paste(ntou, (615,300))
    
    draw = ImageDraw.Draw(Himage2)    
    draw.text((10, 120), sJobPosition, font = font75, fill = 0)
    draw.text((110, 220), sName, font = font150, fill = 0)
    draw.text((600, 225), sStatus, font = font60, fill = 0)
    draw.text((10, 387), sEmail, font = font30, fill = 255)
    draw.text((10, 438), '國立臺灣海洋大學資訊工程學系', font = font30, fill = 0)
    if( int(LineData["newMessNum"]) <=9):
        draw.text((618, 78), str(LineData["newMessNum"]), font = font24, fill = 0)
    else:
        draw.text((608, 78), str(LineData["newMessNum"]), font = font24, fill = 0)
    
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
    '''if len(futureWea[0]) > 4 :
        draw.text((20, 400), (futureWea[0])[0:4], font = font20, fill = 0)
        draw.text((20, 430), (futureWea[0])[5:], font = font20, fill = 0)
    else:
        draw.text((20, 400), futureWea[0], font = font20, fill = 0)'''
    showWeaIcon(Himage2,futureWeaIcon[0], 20, 400)  
    
    
    x = 148
    for i in range(1,7):
        draw.text((x, 160), futureDate[i], font = font24, fill = 0)
        draw.text((x, 200), '溫度', font = font30, fill = 0)
        draw.text((x, 235), futureTemp[i] + '°C' , font = font24, fill = 0)
        draw.text((x, 280), '濕度', font = font30, fill = 0)
        draw.text((x, 315), futureHumi[i] + '%' , font = font24, fill = 0)
        draw.text((x, 360), '天氣', font = font30, fill = 0)
        '''if len(futureWea[i]) > 4 :
            draw.text((x, 400), (futureWea[i])[0:4], font = font20, fill = 0)
            draw.text((x, 430), (futureWea[i])[4:], font = font20, fill = 0)
        else:
            draw.text((x, 400), futureWea[i], font = font20, fill = 0)'''
        showWeaIcon(Himage2, futureWeaIcon[i], x, 400)
        x = x + 110
    
    epd.display(epd.getbuffer(Himage2))

#show page 3
def page3():
    Himage3 = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    
    bmp = Image.open(os.path.join(picdir, 'page3.bmp'))
    bmp = bmp.resize((799,479),Image.BILINEAR)    
    Himage3.paste(bmp, (1,1))
    qrcode = Image.open(os.path.join(picdir, 'qrcode.bmp'))
    qrcode = qrcode.resize((110,110),Image.BILINEAR)    
    Himage3.paste(qrcode, (689,2))    
    
    draw = ImageDraw.Draw(Himage3)
    draw.text((45, 33), '留言板', font = font45, fill = 0)
    messX = 145
    for i in range(1,6):
        
        draw.text((20, messX), jData["No"+ str(i)], font = font24, fill = 0)
        draw.text((135, messX), jData["MessName"+ str(i)], font = font24, fill = 0)
        draw.text((270, messX), jData["Mess"+ str(i)], font = font24, fill = 0)
        messX = messX + 70
        
    epd.display(epd.getbuffer(Himage3))      
    
try:
    #電子紙初始化
    logging.info("epd7in5_V2 Demo")
    epd = epd7in5_V2.EPD()    
    clearPaper()
    
    #字體設定
    font150 = ImageFont.truetype(os.path.join(picdir, 'Font3.ttc'), 150)
    font90 = ImageFont.truetype(os.path.join(picdir, 'Font3.ttc'), 90)
    font75 = ImageFont.truetype(os.path.join(picdir, 'Font3.ttc'), 75)
    font60 = ImageFont.truetype(os.path.join(picdir, 'Font3.ttc'), 60)
    font45 = ImageFont.truetype(os.path.join(picdir, 'Font3.ttc'), 45)
    font30 = ImageFont.truetype(os.path.join(picdir, 'Font3.ttc'), 30)
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font2.ttc'), 24)
    font20 = ImageFont.truetype(os.path.join(picdir, 'Font2.ttc'), 20)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font3.ttc'), 18)   
    
    page1()        
    global page
    page = 1
    nowPageCheck = 0
    while True:
        input = GPIO.input(BTN_PIN)
        currentTime = time.time()
        
        
        #讀取linebotData的Json
        time.sleep(0.1)
        LineDataName = '/home/pi/ePaper_project/mylinebot/ePaperLineBot/lineData.json'
        with open(LineDataName, 'r') as line_object:
            LineData=json.load(line_object)
        with open(jDataName, 'r') as file_object:
            jData=json.load(file_object)
        
        #按鈕更換頁面
        if input == GPIO.LOW and previousStatus == GPIO.HIGH and (currentTime - previousTime) > WAIT_TIME:
            previousTime = currentTime
            page = page + 1
            if page == 4:
                page = 1
            if page == 1:
                page1()
            elif page == 2:
                page2()
            elif page == 3:
                page3()
                watchMessage()
            changePage(page)
        previousStatus = input
        
        if ((LineData["nowPage"] == 1) & (nowPageCheck != 1) ):
            page1()
            page = 1
            nowPageCheck = 1
        elif ((LineData["nowPage"] == 2) & (nowPageCheck != 2) ): 
            page2()
            page = 2
            nowPageCheck = 2
        elif ((LineData["nowPage"] == 3) & (nowPageCheck != 3) ):
            page3()
            page = 3
            nowPageCheck = 3
            watchMessage()
        
        #Linebot修改門牌資料後，進行更新
        if( (sName!= LineData["SaveName"]) | (sJobPosition!= LineData["saveJobTitle"]) | (sStatus!= LineData["saveStatus"]) | (sEmail!= LineData["saveEmail"]) ):
            sName = LineData["SaveName"]
            sJobPosition = LineData["saveJobTitle"]
            sStatus = LineData["saveStatus"]
            sEmail = LineData["saveEmail"]
            getDoorPlate(sName, sJobPosition, sStatus, sEmail)
            page1()
            page = 1
            changePage(page)
        if ((sNewMess!= LineData["newMessNum"]) & (page != 3) ):
            sNewMess = LineData["newMessNum"]
            page1()
            page = 1
            getData()
            changePage(page)
    
except IOError as e:
    logging.info(e)

#使用Ctrl+C打斷程式後，清除電子紙    
except KeyboardInterrupt:    
    print("Exception: KeyboardInterrupt")
    firstPage()
    clearPaper()   
    logging.info("Goto Sleep...")
    epd.sleep()
    epd7in5_V2.epdconfig.module_exit()    
    exit()
    
finally:
    GPIO.cleanup()    
