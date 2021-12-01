"""
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.exceptions import InvalidSignatureError
from linebot import LineBotApi, WebhookHandler
from flask import Flask, request, abort
from mylinebot import settings
from linebot.models.messages import Message
app = Flask(__name__)


# Channel Access Token
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
#line_bot_api = LineBotApi('fdjMrnrqn8Yg7tyS15MkzJj8gZdazZ8uIDOSe6vTzlppJQsPzd3v9LbL6bDrtJfjoGuFSrdgUlNxibXGEZ2y687JT2W7AGvyXffm4Fq42uZkBk/4lgt+YjcjXGhJi6qc8JmcldCWCCc8oVouBzNnawdB04t89/1O/w1cDnyilFU=')

# Channel Secret
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)
#handler = WebhookHandler('6b05c49463ac68ef27496a074551a668')

changeName = False
changeJobTitle = False
changeStatus = False
changeEmail = False
changeRow5 = False


# 監聽所有來自 /callback 的 Post Request

@app.route("/callback", methods=['POST'])
def callback():

    # Get X-Line-Signature header value
    signature = request.headers['X_LINE_SIGNATURE']

    # Get request body as text
    body = request.get_data(as_text=True)

    app.logger.info(f'Request body: {body}')

    # Handle webhook body
    try:
        handler.handle(body, signature)         # 傳入的事件
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=event.message.text))


if (__name__) == '__main__':
    app.run()
"""

"""
def handle_message(event):
    global changeName
    global changeJobTitle
    global changeStatus
    global changeEmail
    global changeRow5
    text = event.message.text
    if changeName == True:
        sheet.update_acell('H1', text)
        changeName = False
        message = TextSendMessage(text=f'已將姓名修改為 - {text}')
        line_bot_api.reply_message(event.reply_token, message)
    elif changeJobTitle == True:
        sheet.update_acell('H2', text)
        changeJobTitle = False
        message = TextSendMessage(text=f'已將職稱修改為 - {text}')
        line_bot_api.reply_message(event.reply_token, message)
    elif changeStatus == True:
        sheet.update_acell('H3', text)
        changeStatus = False
        message = TextSendMessage(text=f'已將狀態修改為 - {text}')
        line_bot_api.reply_message(event.reply_token, message)
    elif changeEmail == True:
        sheet.update_acell('H4', text)
        changeEmail = False
        message = TextSendMessage(text=f'已將Email修改為 - {text}')
        line_bot_api.reply_message(event.reply_token, message)
    elif changeRow5 == True:
        sheet.update_acell('H5', text)
        changeRow5 = False
        message = TextSendMessage(text=f'已將留言修改為 - {text}')
        line_bot_api.reply_message(event.reply_token, message)
    else:
        if text == "!name":
            changeName = True
            message = TextMessage(text="請輸入想要修改的姓名")
            line_bot_api.reply_message(event.reply_token, message)
        elif text == "!job":
            changeJobTitle = True
            message = TextMessage(text="請輸入想要修改的職稱")
            line_bot_api.reply_message(event.reply_token, message)
        elif text == "!status":
            changeStatus = True
            message = TextMessage(text="請輸入想要修改的狀態")
            line_bot_api.reply_message(event.reply_token, message)
        elif text == "!email":
            changeEmail = True
            message = TextMessage(text="請輸入想要修改的Email")
            line_bot_api.reply_message(event.reply_token, message)
        elif text == "!comment":
            changeRow5 = True
            message = TextMessage(text="請輸入想要修改的留言")
            line_bot_api.reply_message(event.reply_token, message)
        else:
            sheet.append_row((1, 2, 3, 4, 5))
            message = TextSendMessage(text="請輸入正確的指令")
            line_bot_api.reply_message(event.reply_token, message)
"""

# 匯入模組
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials as SAC

# 設定 json 檔案路徑及程式操作範圍
Json = '/home/pi/ePaper_project/mylinebot/ePaperLineBot/credentials.json'
Url = ['https://spreadsheets.google.com/feeds']

# 連線至資料表
Connect = SAC.from_json_keyfile_name(Json, Url)
GoogleSheets = gspread.authorize(Connect)

# 開啟資料表及工作表
Sheet = GoogleSheets.open_by_key('1zMuXhbn8SfMWMmP1taeaz850dPxOOdTQPJdW1QkxQp0')
sheet = Sheet.sheet1

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from saveLineData import *

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
        
        global saveName 
        global saveJobPosition 
        global saveStatus
        global saveEmail
        checkCount = 1
        if(checkCount == 1):
            saveName = sheet.acell('B1').value
            saveJobPosition = sheet.acell('B2').value
            saveStatus = sheet.acell('B3').value
            saveEmail = sheet.acell('B4').value
            saveData(saveName,saveJobPosition,saveStatus,saveEmail)
            checkCount = checkCount + 1
        
        messageTotalNum = int(sheet.acell('C8').value) + 1

        for event in  events:

            if isinstance(event, MessageEvent):  # 如果有訊息事件
                text = event.message.text

                if text == "!更改門牌資訊":

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

                elif text == "!電子紙介紹":

                    line_bot_api.reply_message(  # 回復「留言」按鈕樣板訊息
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text='Buttons template',
                            template=ButtonsTemplate(
                                title='在電子紙介紹中選擇介紹內容',
                                text='提供下列資訊內容供您參考',
                                thumbnail_image_url='https://2.bp.blogspot.com/-Gp2_6OZJ1FQ/XASwZmJF9yI/AAAAAAABQZ0/C8dUDl0e_uEWbDjvwNAo8DArlJX4vIaFwCLcBGAs/s800/computer_programming_man.png',
                                actions=[
                                    URITemplateAction(
                                        label='電子紙基本介紹',
                                        uri='https://zh.wikipedia.org/wiki/%E7%94%B5%E5%AD%90%E7%BA%B8'
                                    ),
                                    URITemplateAction(
                                        label='電子紙簡易教學影片',
                                        uri='https://www.youtube.com/watch?v=QU4LxcYIbuE&loop=0'
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

                elif text== "!門牌Email" or text == "！門牌Email":  # 使用指令強制更新電子門牌Email
                    changeEmail = True
                    message = TextMessage(text="請輸入想要修改的Email")
                    line_bot_api.reply_message(event.reply_token, message)

                elif (changeName or changeJobTitle or changeStatus or changeEmail or 
                        newMessStatus or newMessName or newMessages) is True:

                    if changeName == True:                                      # 更新電子門牌姓名
                        sheet.update_acell('B1', text)
                        saveName = text
                        saveData(saveName,saveJobPosition,saveStatus,saveEmail)
                        changeName = False
                        message = TextSendMessage(text=f'已將姓名修改為 - \n【{text}】')
                        line_bot_api.reply_message(event.reply_token, message)

                    elif changeJobTitle == True:                                # 更新電子門牌職稱
                        sheet.update_acell('B2', text)
                        saveJobPosition = text
                        saveData(saveName,saveJobPosition,saveStatus,saveEmail)
                        changeJobTitle = False
                        message = TextSendMessage(text=f'已將職稱修改為 - \n【{text}】')
                        line_bot_api.reply_message(event.reply_token, message)

                    elif changeStatus == True:                                  # 更新電子門牌狀態
                        sheet.update_acell('B3', text)
                        saveStatus = text
                        saveData(saveName,saveJobPosition,saveStatus,saveEmail)
                        changeStatus = False
                        message = TextSendMessage(text=f'已將狀態修改為 - \n【{text}】')
                        line_bot_api.reply_message(event.reply_token, message)

                    elif changeEmail == True:                                   # 更新電子門牌Email
                        sheet.update_acell('B4', text)
                        saveEmail = text
                        saveData(saveName,saveJobPosition,saveStatus,saveEmail)
                        changeEmail = False
                        message = TextSendMessage(text=f'已將Email修改為 - \n【{text}】')
                        line_bot_api.reply_message(event.reply_token, message)

                    elif newMessStatus == True:                                 # 新增本次留言身分
                        if len(text) <= 4:
                            sheetTag = f'D{messageTotalNum}'
                            sheet.update_acell(sheetTag, text)
                            newMessStatus = False
                            message = TextSendMessage(text=f'已將留言身分新增為 - \n【{text}】\n接著請輸入您想要的留言姓名\n(限制五個中文字以內)')
                            line_bot_api.reply_message(event.reply_token, message)

                            newMessName = True
                        else:
                            newMessStatus = False
                            message = TextSendMessage(text='很遺憾，留言身分字數需為四個中文字以內，請重新留言！')
                            line_bot_api.reply_message(event.reply_token, message)

                    elif newMessName == True:                                   # 新增本次留言姓名
                        if len(text) <= 5:
                            sheetTag = f'E{messageTotalNum}'
                            sheet.update_acell(sheetTag, text)
                            newMessName = False
                            message = TextSendMessage(text=f'已將留言姓名新增為 - \n【{text}】\n接著請輸入您想要的留言內容')
                            line_bot_api.reply_message(event.reply_token, message)

                            newMessages = True
                        else:
                            newMessName = False
                            message = TextSendMessage(text='很遺憾，留言姓名字數需為五個中文字以內，請重新留言！')
                            line_bot_api.reply_message(event.reply_token, message)

                    elif newMessages == True:                                   # 新增本次留言內容
                        sheetTag = f'F{messageTotalNum}'
                        sheet.update_acell(sheetTag, text)

                        newMessages = False
                        message = TextSendMessage(text=f'已將留言內容新增為：\n{text}')
                        line_bot_api.reply_message(event.reply_token, message)

                        messageSerialNum = int(sheet.acell('C6').value) + 1
                        sheet.update_acell('C6', messageSerialNum)
                        print(f'留言板本次已經有{messageSerialNum}則新留言。')

                        sheet.update_acell('C8', messageTotalNum)
                        print(f'留言板歷史目前已經有{messageTotalNum}則留言。')

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
                                            #text='是，需要匿名。',
                                            data='匿名留言'
                                        ),
                                        PostbackTemplateAction(
                                            label='否,實名。',
                                            #text='否，實名留言。',
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
        
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
