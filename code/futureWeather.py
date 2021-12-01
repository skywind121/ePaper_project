import urllib.request as req
import json 
url3="https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-091?Authorization=rdec-key-123-45678-011121314"

with req.urlopen(url3) as res3:
  futureWeather=json.load(res3)
    
keelung = futureWeather["records"]["locations"][0]["location"][12]
keelungName = keelung["locationName"]

tempCatch = keelung["weatherElement"][1]["time"]
humiCatch = keelung["weatherElement"][2]["time"]
weatherCatch= keelung["weatherElement"][6]["time"]
futureDate = [0]*7
futureTemp = [0]*7
futureHumi = [0]*7
futureWea = [0]*7
futureWeaIcon = [0]*7
count = 0
for i in range(0,14,2):
	futureDate[count] = (tempCatch[i]["startTime"])[5:10]
	futureTemp[count] = tempCatch[i]["elementValue"][0]["value"]
	futureHumi[count] = humiCatch[i]["elementValue"][0]["value"]
	futureWea[count] = weatherCatch[i]["elementValue"][0]["value"]
	futureWeaIcon[count] = weatherCatch[i]["elementValue"][1]["value"]
	count = count+1

#test data	
for j in range(0,7):
	print("Date:" + futureDate[j] + " Temp:" + futureTemp[j] 
	+ "°C Humi:" + futureHumi[j] + "% Weather:" + futureWea[j])
