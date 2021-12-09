# 匯入模組
import gspread
import json
import time
from oauth2client.service_account import ServiceAccountCredentials as SAC

# 設定 json 檔案路徑及程式操作範圍
Json = 'credentials.json'
Url = ['https://spreadsheets.google.com/feeds']

# 連線至資料表
Connect = SAC.from_json_keyfile_name(Json, Url)
GoogleSheets = gspread.authorize(Connect)

# 開啟資料表及工作表
Sheet = GoogleSheets.open_by_key('1zMuXhbn8SfMWMmP1taeaz850dPxOOdTQPJdW1QkxQp0')
sheet = Sheet.sheet1

def getData():
	global jobPosition,showName,nowStatus,mark,email, pageNum,newMessageNum 
	#讀取名牌資訊
	jobPosition = sheet.acell('B2').value
	showName = sheet.acell('B1').value
	nowStatus = sheet.acell('B3').value
	email = sheet.acell('B4').value
	mark = sheet.acell('C8').value
	markInt = int(mark)
	pageNum = sheet.acell('B5').value
	newMessageNum = int(sheet.acell('C6').value)
	
	
	#設置討論區的系級、名字還有留言内容的string
	global no,name,mess
	no = [0]*5
	name = [0]*5
	mess = [0]*5
	
	messCount = 0
	#讀取討論區資料
	for markInt in range(markInt,markInt-5,-1):
		markString = str(markInt)
		no[messCount] = sheet.acell('D'+markString).value
		name[messCount] = sheet.acell('E'+markString).value
		mess[messCount] = sheet.acell('F'+markString).value
		messCount = messCount + 1
	saveJson(newMessageNum)
	
def firstPage():
	sheet.update_acell('B5', '1')
	
def getDoorPlate(newName, newJob, newStatus, newMail):
	global jobPosition,showName,nowStatus,mark,email, pageNum,newMessageNum 
	pageNum = sheet.acell('B5').value
	newMessageNum = int(sheet.acell('C6').value)
	showName = newName
	jobPosition = newJob
	nowStatus = newStatus
	email = newMail
	saveJson(newMessageNum)

def watchMessage():
	newMessageNum = 0
	sheet.update_acell('C6', newMessageNum)
	saveJson(newMessageNum)
	
	linejdata = {	"SaveName": showName,
					"saveJobTitle": jobPosition,
					"saveStatus": nowStatus,
					"saveEmail": email,
					"nowPage": pageNum,
					"newMessNum": newMessageNum
				}
	with open('/home/pi/ePaper_project/mylinebot/ePaperLineBot/lineData.json', 'w', encoding = 'utf-8') as f:
		json.dump(linejdata, f, ensure_ascii=False)
	
	#print("0:" + newMessageNum)

def changePage(pageNum):
	sheet.update_acell('B5', str(pageNum))

def saveJson(newMessageNum):
	jData = {	
			"ShowName": str(showName),
			"JobPosition": jobPosition,
			"Status": nowStatus,
			"email": email,
			"No1": no[0],
			"MessName1": name[0],
			"Mess1": mess[0],
			"No2": no[1],
			"MessName2": name[1],
			"Mess2": mess[1],
			"No3": no[2],
			"MessName3": name[2],
			"Mess3": mess[2],
			"No4": no[3],
			"MessName4": name[3],
			"Mess4": mess[3],
			"No5": no[4],
			"MessName5": name[4],
			"Mess5": mess[4],
			"newMessageNum" : newMessageNum
			}
	with open('jsonData.json', 'w', encoding = 'utf-8') as f:
		json.dump(jData, f, ensure_ascii=False)
	#print(newMessageNum)
	
try:
	getData()
	#測試資料能否讀取到
	'''for j in range(0,5):
		print(no[j] + ':' + name[j] + ':' + mess[j])'''
		
except KeyboardInterrupt:    
    print("Exception: KeyboardInterrupt")
    exit()

