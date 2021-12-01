import json

def saveData():
	linejdata = {	"ShowName": 'saveName77',
					"JobPosition": 'saveJobPosition',
					"Status": 'saveStatus',
					"email": 'saveEmail'
				}
	with open('/home/pi/ePaper_project/mylinebot/ePaperLineBot/lineData.json', 'w', encoding = 'utf-8') as f:
		json.dump(linejdata, f, ensure_ascii=False)

saveData()
