import json

def saveData(sName,sJobPosition,sStatus,sEmail):
	linejdata = {	"SaveName": sName,
					"saveJobPosition": sJobPosition,
					"saveStatus": sStatus,
					"saveEmail": sEmail
				}
	with open('/home/pi/ePaper_project/mylinebot/ePaperLineBot/lineData.json', 'w', encoding = 'utf-8') as f:
		json.dump(linejdata, f, ensure_ascii=False)

