# 匯入模組
from datetime import time
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials as SAC

# 設定 json 檔案路徑及程式操作範圍
Json = '/home/pi/ePaper_project/mylinebot/ePaperLineBot/credentials.json'
#Json = 'D:\Desktop\IndependentStudy\mylinebot\ePaperLineBot\credentials.json'
Url = ['https://spreadsheets.google.com/feeds']

# 連線至資料表
Connect = SAC.from_json_keyfile_name(Json, Url)
GoogleSheets = gspread.authorize(Connect)

# 開啟資料表及工作表
Sheet = GoogleSheets.open_by_key('1zMuXhbn8SfMWMmP1taeaz850dPxOOdTQPJdW1QkxQp0')
sheet = Sheet.sheet1

import datetime
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.utils import timezone
from saveLineData import *
from ePaperLineBot.models import *


from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (MessageEvent, TextMessage, TextSendMessage, 
TemplateSendMessage, ButtonsTemplate, ConfirmTemplate, MessageTemplateAction,
PostbackEvent, PostbackTemplateAction, URITemplateAction) 
 
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

changeName = False
changeJobTitle = False
changeStatus = False
changeEmail = False
newMessStatus = False
newMessName = False
newMessages = False
newUserLogin = False
globalTrueName = ''

saveName = sheet.acell('B1').value
saveJobTitle = sheet.acell('B2').value
saveStatus = sheet.acell('B3').value
saveEmail = sheet.acell('B4').value
displayPage = sheet.acell('B5').value
newMess = sheet.acell('C6').value
saveData(saveName, saveJobTitle, saveStatus, saveEmail, displayPage, newMess)

@csrf_exempt
def callback(request):
    
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
 
        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        global changeName
        global changeJobTitle
        global changeStatus
        global changeEmail
        global newMessStatus
        global newMessName
        global newMessages
        global newUserLogin
        global globalTrueName
        
        global saveName 
        global saveJobTitle 
        global saveStatus
        global saveEmail
        global displaypage
        global newMess
        
        displayPage = sheet.acell('B5').value
        messageTotalNum = int(sheet.acell('C8').value) + 1

        for event in  events:

            if isinstance(event, MessageEvent):  # 如果有訊息事件
                text = event.message.text
                uid = event.source.user_id
                profile = line_bot_api.get_profile(uid)
                lineName = profile.display_name
                
                if text == "!上一頁" or text == "！上一頁":

                    displayPage = int(sheet.acell('B5').value)
                    if 1 < displayPage and displayPage <= 3:
                        sheet.update_acell('B5', str(displayPage - 1))
                    else:                                           # displayPage == 1
                        displayPage = 4
                        sheet.update_acell('B5', str(displayPage - 1))
                        
                    saveData(saveName, saveJobTitle, saveStatus, saveEmail, displayPage-1, newMess)
                    message = TextSendMessage(text=f'電子門牌第{displayPage - 1}頁面已顯示。')
                    line_bot_api.reply_message(event.reply_token, message)

                elif text == "!下一頁" or text == "！下一頁":

                    displayPage = int(sheet.acell('B5').value)
                    if 1 <= displayPage and displayPage < 3:
                        sheet.update_acell('B5', str(displayPage + 1))
                    else:                                           # displayPage == 3
                        displayPage = 0
                        sheet.update_acell('B5', str(displayPage + 1))
                    
                    saveData(saveName, saveJobTitle, saveStatus, saveEmail, displayPage+1, newMess)
                    message = TextSendMessage(text=f'電子門牌第{displayPage + 1}頁面已顯示。')
                    line_bot_api.reply_message(event.reply_token, message)

                if text == "!更改門牌資訊":

                    if User_Info.objects.filter(uid = uid).exists() == False:
                        message = TextSendMessage(text=f'{lineName}您好，需要您先經過\n【登入確認】後才能使用\n【更改門牌資料】功能。')
                        line_bot_api.reply_message(event.reply_token, message)

                    else:
                        line_bot_api.reply_message(  # 回覆「更改門牌資料」按鈕樣板訊息
                            event.reply_token,
                            TemplateSendMessage(
                                alt_text='Buttons template',
                                template=ButtonsTemplate(
                                    title='請選擇需要更改的電子門牌資訊',
                                    text='提供下列資訊更動',
                                    thumbnail_image_url='https://4.bp.blogspot.com/-AsbF3HjHxBQ/VCOJkZJrFyI/AAAAAAAAmzQ/0P6nUTbrABo/s800/school_sensei_kokuban.png',
                                    actions=[
                                        PostbackTemplateAction(
                                            label='門牌姓名',
                                            #text='!門牌姓名',
                                            data='A&門牌姓名'
                                        ),
                                        PostbackTemplateAction(
                                            label='門牌職稱',
                                            #text='!門牌職稱',
                                            data='A&門牌職稱'
                                        ),
                                        PostbackTemplateAction(
                                            label='門牌狀態',
                                            #text='!門牌狀態',
                                            data='A&門牌狀態'
                                        ),
                                        PostbackTemplateAction(
                                            label='門牌Email',
                                            #text='!門牌Email',
                                            data='A&門牌Email'
                                        )
                                    ]
                                )
                            )
                        )

                elif text == "!留言板發言":

                    line_bot_api.reply_message(  # 回復「留言」按鈕樣板訊息
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text='Buttons template',
                            template=ButtonsTemplate(
                                title='在留言板中新增留言',
                                text='請先選擇您的身分',
                                thumbnail_image_url='https://2.bp.blogspot.com/-H2eLSLfzvpA/XGjx1UapC6I/AAAAAAABRcA/5Xdh-W7tqk8X1YONndv2B1ykhJ6BRS1bgCLcBGAs/s800/ai_computer_sousa_robot.png',
                                actions=[
                                    PostbackTemplateAction(
                                        label='學生',
                                        #text='!門牌姓名',
                                        data='B&學生'
                                    ),
                                    PostbackTemplateAction(
                                        label='教職員',
                                        #text='!門牌職稱',
                                        data='B&教職員'
                                    ),
                                    PostbackTemplateAction(
                                        label='行政人員',
                                        #text='!門牌狀態',
                                        data='B&行政人員'
                                    ),
                                    PostbackTemplateAction(
                                        label='其他',
                                        #text='!門牌Email',
                                        data='B&其他'
                                    )
                                ]
                            )
                        )
                    )

                elif text == "!登入嘗試":

                    line_bot_api.reply_message(  # 回復「留言」按鈕樣板訊息
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text='Buttons template',
                            template=ButtonsTemplate(
                                title='您是否在過去已經登入過了？',
                                text='請選擇您的登入方式',
                                #thumbnail_image_url='https://imgur.com/9RnuZjX.png',
                                thumbnail_image_url='https://4.bp.blogspot.com/-H4YfqE0zNr8/WwofRfOyapI/AAAAAAABMYA/h97Wvj7YYQYLslHxT3VIKFSZjxWazMMBQCLcBGAs/s800/internet_gazou_ninsyou.png',
                                actions=[
                                    PostbackTemplateAction(
                                        label='初次登入',
                                        data='C&初次登入'
                                    ),
                                    PostbackTemplateAction(
                                        label='登入確認',
                                        data='C&登入確認'
                                    )
                                ]
                            )
                        )
                    )

                elif text == "!電子紙介紹":

                    line_bot_api.reply_message(  # 回復「留言」按鈕樣板訊息
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text='Buttons template',
                            template=ButtonsTemplate(
                                title='在電子紙介紹中選擇介紹內容',
                                text='提供下列資訊內容供您參考',
                                #thumbnail_image_url='https://i.imgur.com/dPj1VJl.png',
                                thumbnail_image_url='https://2.bp.blogspot.com/-Gp2_6OZJ1FQ/XASwZmJF9yI/AAAAAAABQZ0/C8dUDl0e_uEWbDjvwNAo8DArlJX4vIaFwCLcBGAs/s800/computer_programming_man.png',
                                actions=[
                                    URITemplateAction(
                                        label='電子紙基本介紹',
                                        uri='https://zh.wikipedia.org/wiki/%E7%94%B5%E5%AD%90%E7%BA%B8'
                                    ),
                                    URITemplateAction(
                                        label='電子紙簡易教學影片',
                                        uri='https://www.youtube.com/watch?v=QU4LxcYIbuE&loop=0'
                                    ),
                                    URITemplateAction(
                                        label='本專題使用電子門牌 Demo 影片',
                                        uri='https://www.youtube.com/watch?v=PYQZwgQVwiU&loop=0'
                                    )
                                ]
                            )
                        )
                    )    

                elif text == "!門牌姓名" or text == "！門牌姓名":  # 使用指令強制更新電子門牌姓名
                    changeName = True
                    message = TextMessage(text="請輸入想要修改的姓名")
                    line_bot_api.reply_message(event.reply_token, message)

                elif text == "!門牌職稱" or text == "！門牌職稱":  # 使用指令強制更新電子門牌職稱
                    changeJobTitle = True
                    message = TextMessage(text="請輸入想要修改的職稱")
                    line_bot_api.reply_message(event.reply_token, message)

                elif text == "!門牌狀態" or text == "！門牌狀態":  # 使用指令強制更新電子門牌狀態
                    changeStatus = True
                    message = TextMessage(text="請輸入想要修改的狀態")
                    line_bot_api.reply_message(event.reply_token, message)

                elif text == "!門牌Email" or text == "！門牌Email":  # 使用指令強制更新電子門牌Email
                    changeEmail = True
                    message = TextMessage(text="請輸入想要修改的Email")
                    line_bot_api.reply_message(event.reply_token, message)

                elif (changeName or changeJobTitle or changeStatus or changeEmail or 
                        newMessStatus or newMessName or newMessages or newUserLogin) is True:

                    if changeName == True:                                      # 更新電子門牌姓名
                        sheet.update_acell('B1', text)
                        saveName = text
                        saveData(saveName, saveJobTitle, saveStatus, saveEmail, displayPage, newMess)
                        changeName = False
                        message = TextSendMessage(text=f'已將姓名修改為 - \n【{text}】')
                        line_bot_api.reply_message(event.reply_token, message)

                    elif changeJobTitle == True:                                # 更新電子門牌職稱
                        sheet.update_acell('B2', text)
                        saveJobTitle = text
                        saveData(saveName, saveJobTitle, saveStatus, saveEmail, displayPage, newMess)
                        changeJobTitle = False
                        message = TextSendMessage(text=f'已將職稱修改為 - \n【{text}】')
                        line_bot_api.reply_message(event.reply_token, message)

                    elif changeStatus == True:                                  # 更新電子門牌狀態
                        sheet.update_acell('B3', text)
                        saveStatus = text
                        saveData(saveName, saveJobTitle, saveStatus, saveEmail, displayPage, newMess)
                        changeStatus = False
                        message = TextSendMessage(text=f'已將狀態修改為 - \n【{text}】')
                        line_bot_api.reply_message(event.reply_token, message)

                    elif changeEmail == True:                                   # 更新電子門牌Email
                        sheet.update_acell('B4', text)
                        saveEmail = text
                        saveData(saveName, saveJobTitle, saveStatus, saveEmail, displayPage, newMess)
                        changeEmail = False
                        message = TextSendMessage(text=f'已將Email修改為 - \n【{text}】')
                        line_bot_api.reply_message(event.reply_token, message)

                    elif newMessStatus == True:                                 # 新增本次留言身分
                        if len(text) <= 4:
                            sheetTag = f'D{messageTotalNum}'
                            sheet.update_acell(sheetTag, text)
                            newMessStatus = False

                            message = []
                            message.append(TextSendMessage(text=f'已將留言身分新增為 - \n【{text}】'))
                            message.append(
                                    TemplateSendMessage(
                                    alt_text='Confirm template',
                                    template=ConfirmTemplate(
                                        text=f'{text}您好，請問本次留言需要匿名嗎？',
                                        actions=[
                                            PostbackTemplateAction(  # 將第一步驟選擇的地區，包含在第二步驟的資料中
                                                label='是,匿名。',
                                                data='匿名留言'
                                            ),
                                            PostbackTemplateAction(
                                                label='否,實名。',
                                                data='實名留言'
                                            )
                                        ]
                                    )
                                )
                            )
                            line_bot_api.reply_message(event.reply_token, message)
                        else:
                            newMessStatus = False
                            message = TextSendMessage(text='很遺憾，留言身分字數需為\n四個中文字以內，請重新留言！')
                            line_bot_api.reply_message(event.reply_token, message)

                    elif newMessName == True:                                   # 新增本次留言姓名
                        if len(text) <= 5:
                            sheetTag = f'E{messageTotalNum}'
                            sheet.update_acell(sheetTag, text)
                            newMessName = False

                            message = []
                            message.append(TextSendMessage(text=f'已將留言姓名新增為 - \n【{text}】'))
                            message.append(TextSendMessage(text=f'請輸入您想要的留言內容'))
                            line_bot_api.reply_message(event.reply_token, message)

                            newMessages = True
                        else:
                            newMessName = False
                            message = TextSendMessage(text='很遺憾，留言姓名字數需為\n五個中文字以內，請重新留言！')
                            line_bot_api.reply_message(event.reply_token, message)

                    elif newMessages == True:                                   # 新增本次留言內容
                        sheetTag = f'F{messageTotalNum}'
                        sheet.update_acell(sheetTag, text)

                        newMessages = False
                        message = TextSendMessage(text=f'已將留言內容新增為：\n{text}')
                        line_bot_api.reply_message(event.reply_token, message)

                        messageSerialNum = int(sheet.acell('C6').value) + 1
                        sheet.update_acell('C6', messageSerialNum)
                        saveData(saveName, saveJobTitle, saveStatus, saveEmail, displayPage, messageSerialNum)
                        print(f'留言板本次已經有{messageSerialNum}則新留言。')

                        sheet.update_acell('C8', messageTotalNum)
                        print(f'留言板歷史目前已經有{messageTotalNum}則留言。')

                    elif newUserLogin == True:                                   # 新增本次使用者資訊                        
                        #uid = event.source.user_id                              # user_id
                        profile = line_bot_api.get_profile(uid)
                        #lineName = profile.display_name                         # LINE的名字
                        userTrueName = event.message.text                        # 使用者真實姓名
                        globalTrueName = userTrueName
                        pic_url = profile.picture_url                            # 大頭貼網址
                        mdt = datetime.datetime.now().strftime('%Y{y}%m{m}%d{d} %H{h}%M{f}%S{s}').format(y='年',m='月',d='日',h='時',f='分',s='秒')                            # 登入資訊物件創建的日期時間
                        
                        message = []
                        if User_Info.objects.filter(uid = uid).exists() == False:
                            User_Info.objects.create(uid = uid, lineName = lineName, userTrueName = userTrueName, pic_url = pic_url, mdt = mdt)
                            message = TextSendMessage(text=f'{userTrueName}教授您好，\n您的會員資料已新增完畢！')
                            line_bot_api.reply_message(event.reply_token,message)

                        newUserLogin = False

            elif isinstance(event, PostbackEvent):  # 如果有回傳值事件
 
                if event.postback.data[0:1] == "A":  # 如果回傳值為「選擇更改」
 
                    info = event.postback.data[2:]  # 透過切割字串取得更改資訊的文字
 
                    line_bot_api.reply_message(   # 回復「選擇更改資訊類別」按鈕樣板訊息
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text='Buttons template',
                            template=ButtonsTemplate(
                                title='請選擇需要更改的電子門牌資訊',
                                text=f'確定要更改 {info} 的資訊嗎？',
                                actions=[
                                    PostbackTemplateAction(  # 將第一步驟選擇的地區，包含在第二步驟的資料中
                                        label='是，我要更改。',
                                        #text=f'!{info}',
                                        data=f'!{info}'
                                    ),
                                    PostbackTemplateAction(
                                        label='否，我再想想。',
                                        #text='否，我再想想。',
                                        data='NO'
                                    )
                                ]
                            )
                        )
                    )
 

                elif event.postback.data == "!門牌姓名":  # 如果回傳值為「是，我要更改。」
                    changeName = True
                    message = TextMessage(text="請輸入想要修改的姓名")
                    line_bot_api.reply_message(event.reply_token, message)
                elif event.postback.data == "!門牌職稱":  # 如果回傳值為「是，我要更改。」
                    changeJobTitle = True
                    message = TextMessage(text="請輸入想要修改的職稱")
                    line_bot_api.reply_message(event.reply_token, message)
                elif event.postback.data == "!門牌狀態":  # 如果回傳值為「是，我要更改。」
                    changeStatus = True
                    message = TextMessage(text="請輸入想要修改的狀態")
                    line_bot_api.reply_message(event.reply_token, message)
                elif event.postback.data == "!門牌Email":  # 如果回傳值為「是，我要更改。」
                    changeEmail = True
                    message = TextMessage(text="請輸入想要修改的Email")
                    line_bot_api.reply_message(event.reply_token, message)


                elif event.postback.data == "NO":  # 如果回傳值為「否，我再想想。」
                    message = TextSendMessage(text='歡迎重新設定門牌資訊！')
                    line_bot_api.reply_message(event.reply_token, message)

                 
                elif event.postback.data[0:1] == "B":  # 如果回傳值為「新增留言」
                    
                    messStatus = event.postback.data[2:]  # 透過切割字串取得更改資訊的文字

                    if messStatus == '其他':
                        newMessStatus = True
                        message = TextMessage(text="請輸入您想要的留言身分\n(限制四個中文字以內)")
                        line_bot_api.reply_message(event.reply_token, message)
                    else:
                        sheetTag = f'D{messageTotalNum}'
                        sheet.update_acell(sheetTag, messStatus)

                        line_bot_api.reply_message(   # 回復「選擇更改資訊類別」按鈕樣板訊息
                            event.reply_token,
                            TemplateSendMessage(
                                alt_text='Confirm template',
                                template=ConfirmTemplate(
                                    text=f'{messStatus}您好，請問本次留言需要匿名嗎？',
                                    actions=[
                                        PostbackTemplateAction(  # 將第一步驟選擇的地區，包含在第二步驟的資料中
                                            label='是,匿名。',
                                            data='匿名留言'
                                        ),
                                        PostbackTemplateAction(
                                            label='否,實名。',
                                            data='實名留言'
                                        )
                                    ]
                                )
                            )
                        )

                elif event.postback.data == "匿名留言":  # 如果回傳值為「是，我要更改。」
                    sheetTag = f'E{messageTotalNum}'
                    sheet.update_acell(sheetTag, '匿名')
                    newMessages = True
                    message = TextMessage(text="請輸入您想要的留言內容")
                    line_bot_api.reply_message(event.reply_token, message)

                elif event.postback.data == "實名留言":  # 如果回傳值為「是，我要更改。」
                    newMessName = True
                    message = TextMessage(text="請輸入您想要的留言姓名\n(限制五個中文字以內)")
                    line_bot_api.reply_message(event.reply_token, message)

                elif event.postback.data[0:1] == "C":  # 如果回傳值為「新增留言」
                    
                    memberLogin = event.postback.data[2:]  # 透過切割字串取得更改資訊的文字

                    if memberLogin == '初次登入':
                        newUserLogin = True
                        uid = event.source.user_id                               # user_id
                        profile = line_bot_api.get_profile(uid)
                        lineName = profile.display_name                          # LINE的名字
                        #userTrueName = globalTrueName                            # 使用者真實姓名
                        user_info = User_Info.objects.filter(uid = uid)

                        if User_Info.objects.filter(uid = uid).exists() == False:
                            message = TextMessage(text=f'{lineName}教授您好，\n請輸入您的真實姓名')
                            line_bot_api.reply_message(event.reply_token, message)
                        else:
                            message = TextSendMessage(text=f'{user_info[0].userTrueName}教授您好，\n您已經有建立會員資料囉！\n請點選【登入確認】查看！')
                            line_bot_api.reply_message(event.reply_token,message)

                    elif memberLogin == '登入確認':
                        message = []
                        message.append(TextMessage(text="正在確認您的資料……"))
                        
                        uid = event.source.user_id                               # user_id
                        profile = line_bot_api.get_profile(uid)
                        lineName = profile.display_name                          # LINE的名字
                        #userTrueName = globalTrueName                            # 使用者真實姓名
                        pic_url = profile.picture_url                            # 大頭貼網址
                        mdt = datetime.datetime.now()                            # 登入資訊物件創建的日期時間

                        if User_Info.objects.filter(uid = uid).exists() == True:
                            user_info = User_Info.objects.filter(uid = uid)
                            message.append(TextSendMessage(text=f'{user_info[0].userTrueName}教授您好，\n您已經有建立會員資料囉！'))
                            for user in user_info:
                                user.mdt = user.mdt.strftime('%Y{y}%m{m}%d{d} %H{h}%M{f}%S{s}').format(y='年',m='月',d='日',h='時',f='分',s='秒')
                                info = f'您的會員資料如下： \
                                        ------------------------------ \
                                        UID is 【{user.uid}】\
                                        ------------------------------ \
                                        Line Name is 【{user.lineName}】\
                                        ------------------------------ \
                                        Full Name is 【{user.userTrueName}】\
                                        ------------------------------ \
                                        Creation time of info object is 【{user.mdt}】'
                                message.append(TextSendMessage(text = info))
                                line_bot_api.reply_message(event.reply_token,message)
                        else:
                            message.append(TextSendMessage(text=f'{lineName}教授您好，\n您尚未建立會員資料，\n請點選【初次登入】'))

                        line_bot_api.reply_message(event.reply_token, message)
        
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
