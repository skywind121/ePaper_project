#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
    
#ePaper library
import logging
import time
from waveshare_epd import epd7in5_V2
from PIL import Image,ImageDraw,ImageFont
import traceback

from data import *  #input the googlesheet data

logging.basicConfig(level=logging.DEBUG)

#clean ePaper 
def clearPaper():
    logging.info("Clear...")
    epd.init()
    epd.Clear()
 
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
    for i in range(0,5):
        draw.text((20, messX), no[i], font = font24, fill = 0)
        draw.text((160, messX), name[i], font = font24, fill = 0)
        draw.text((270, messX), mess[i], font = font24, fill = 0)
        messX = messX + 70
        
    epd.display(epd.getbuffer(Himage3))


except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    print("Exception: KeyboardInterrupt")
    epd7in5_V2.epdconfig.module_exit()
    exit()
