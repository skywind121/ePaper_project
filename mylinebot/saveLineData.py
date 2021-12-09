import json

def saveData(sName, sJobTitle, sStatus, sEmail, pageShow, newMessNum):
	linejdata = {	"SaveName": sName,
					"saveJobTitle": sJobTitle,
					"saveStatus": sStatus,
					"saveEmail": sEmail,
					"nowPage": pageShow,
					"newMessNum": int(newMessNum)
				}
	with open('/home/pi/ePaper_project/mylinebot/ePaperLineBot/lineData.json', 'w', encoding = 'utf-8') as f:
		json.dump(linejdata, f, ensure_ascii=False)
	'''with open('D:\Desktop\IndependentStudy\mylinebot\ePaperLineBot\lineData.json', 'w', encoding = 'utf-8') as f:
		json.dump(linejdata, f, ensure_ascii=False)'''



