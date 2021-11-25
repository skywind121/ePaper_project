import gspread
creds = gspread.service_account(filename='credentials.json')
client = creds.open_by_url(
"https://docs.google.com/spreadsheets/d/1zMuXhbn8SfMWMmP1taeaz850dPxOOdTQPJdW1QkxQp0/edit#gid=0")
sheet = client.get_worksheet(0)  # get the first sheet, idx=0

jobPosition = sheet.acell('D1').value
showName = sheet.acell('D2').value
nowStatus = sheet.acell('D3').value
mark = sheet.acell('E1').value
markInt = int(mark)

no = [0]*5
name = [0]*5
mess = [0]*5
messCount = 0
for markInt in range(markInt,markInt-5,-1):
	markString = str(markInt)
	no[messCount] = sheet.acell('A'+markString).value
	name[messCount] = sheet.acell('B'+markString).value
	mess[messCount] = sheet.acell('C'+markString).value
	messCount = messCount + 1

'''for j in range(0,5):
	print(no[j] + ':' + name[j] + ':' + mess[j])'''
