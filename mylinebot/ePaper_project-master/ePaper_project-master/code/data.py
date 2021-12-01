# 匯入模組
import gspread
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
	global jobPosition,showName,nowStatus,mark
	#讀取名牌資訊
	jobPosition = sheet.acell('D1').value
	showName = sheet.acell('D2').value
	nowStatus = sheet.acell('D3').value
	mark = sheet.acell('E1').value
	markInt = int(mark)
	
	#設置討論區的系級、名字還有留言内容的string
	global no,name,mess
	no = [0]*5
	name = [0]*5
	mess = [0]*5
	
	messCount = 0
	#讀取討論區資料
	for markInt in range(markInt,markInt-5,-1):
		markString = str(markInt)
		no[messCount] = sheet.acell('A'+markString).value
		name[messCount] = sheet.acell('B'+markString).value
		mess[messCount] = sheet.acell('C'+markString).value
		messCount = messCount + 1
		
try:
	getData()

	#測試資料能否讀取到
	for j in range(0,5):
		print(no[j] + ':' + name[j] + ':' + mess[j])
		
except KeyboardInterrupt:    
    print("Exception: KeyboardInterrupt")
    exit()

