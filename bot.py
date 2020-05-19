import telebot
from telebot import apihelper
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from telebot import types
import schedule,threading
import time
from apiclient import errors
from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools


admin_id = input("Enter admin telegram ID\n")
table_data = input("Enter data table ID\n")

users_table = "1Ztgxri6dYyKAZ0nPdmPndjDG9BR8W0qvZOcQGYEjrj0"



bot = telebot.TeleBot('916360104:AAHIK81ItJUb7FLaEe-1TWKxt4leCXss9UI')
messages=[]
channels={}
calldata=[]
admin_channelId = 0






CREDENTIALS_FILE = 'credentials1.json'  # Имя файла с закрытым ключом, вы должны подставить свое

# Читаем ключи из файла
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/drive.photos.readonly'])

httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth) # Выбираем работу с таблицами и 4 версию API


spreadsheetId = table_data # сохраняем идентификатор файла
print('https://docs.google.com/spreadsheets/d/' + spreadsheetId)

# SCOPES = 'https://www.googleapis.com/auth/drive.photos.readonly'

# store = file.Storage('storage.json')
# creds = store.get()
# if not creds or creds.invalid:
# 	flow = client.flow_from_clientsecrets('credentials1.json', SCOPES)
# 	creds = tools.run_flow(flow, store)

# driveService = discovery.build('drive', 'v3', http=creds.authorize(Http()))

# print(driveService)
# page_token = None
# while True:
# 	print("1")
# 	response = driveService.files().list(q="mimeType='images/jpeg'",
# 										  spaces='photos',
# 										  fields='nextPageToken, files(id, name)',
# 										  pageToken=page_token).execute()
# 	for file in response.get('files', []):
# 		print(file.get('link'))
# 		photos1.append(file.get('name'))
# 		photos2.append(file.get('id'))
# 		print('Found file: %s (%s)' % (file.get('name'), file.get('id')))
# 	page_token = response.get('nextPageToken', None)
# 	if page_token is None:
# 		print("2")
# 		break


driveService = apiclient.discovery.build('drive', 'v3', http = httpAuth) # Выбираем работу с Google Drive и 3 версию API
access = driveService.permissions().create(
	fileId = spreadsheetId,
	body = {'type': 'user', 'role': 'writer', 'emailAddress': 'ringoagent0905@gmail.com'},  # Открываем доступ на редактирование
	fields = 'id'
).execute()

spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheetId).execute()
sheetList = spreadsheet.get('sheets')
for sheet in sheetList:
	print(sheet['properties']['sheetId'], sheet['properties']['title'])

sheetId = sheetList[0]['properties']['sheetId']

print('Мы будем использовать лист с Id = ', sheetId)
ranges = ["Лист1!A:E"]  #
def job():
    sheet_values=[]
    results = service.spreadsheets().values().batchGet(spreadsheetId=spreadsheetId,
    												   ranges=ranges,
    												   valueRenderOption='FORMATTED_VALUE',
    												   dateTimeRenderOption='FORMATTED_STRING').execute()
    try:
        sheet_values = results['valueRanges'][0]['values']
    except KeyError:
        pass
    return sheet_values

credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])

httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth) # Выбираем работу с таблицами и 4 версию API

spreadsheetId1 = users_table # сохраняем идентификатор файла

driveService = apiclient.discovery.build('drive', 'v3', http = httpAuth) # Выбираем работу с Google Drive и 3 версию API
access = driveService.permissions().create(
	fileId = spreadsheetId1,
	body = {'type': 'user', 'role': 'writer', 'emailAddress': 'ringoagent0905@gmail.com'},  # Открываем доступ на редактирование
	fields = 'id'
).execute()



spreadsheet1 = service.spreadsheets().get(spreadsheetId=spreadsheetId1).execute()
sheetList1 = spreadsheet1.get('sheets')
for sheet in sheetList1:
	print(sheet['properties']['sheetId'], sheet['properties']['title'])

sheetId1 = sheetList1[0]['properties']['sheetId']

print('Мы будем использовать лист с Id = ', sheetId1)
ranges1 = ["Лист1!A:B"]  #

results1 = service.spreadsheets().values().batchGet(spreadsheetId=spreadsheetId1,
												   ranges=ranges1,
												   valueRenderOption='FORMATTED_VALUE',
												   dateTimeRenderOption='FORMATTED_STRING').execute()

sheet_values1 = results1['valueRanges'][0]['values']
sheetv=[]
for i in sheet_values1:
	for i2 in i:
		sheetv.append(i2)

print(sheetv)


# def job(channels):
#   try:
#       if channels[0]:
#           bot.send_message(channels[0], "2")
#   except:
#       if IndexError:
#           pass

# @bot.message_handler(content_types=['text'])
# def job():
# 	print(channels,messages)
# 	for z in channels:
# 		for i in messages:

# 			bot.delete_message(chat_id=z,message_id=i)
# 	bot.send_message(764025058, "2")
sheet_values=job()
@bot.message_handler(commands=['start'])
def start_message(message):

	if message.from_user.username in sheetv:
		bot.send_message(message.chat.id, 'Привет, ты написал мне /start')
		channels[message.chat.id]=[]

		@bot.message_handler(content_types=['sticker'])
		def send_sticker(message):
			print(message)


		@bot.message_handler(content_types=['text'])
		def send_text(message):
			message1=""
			if message.text.lower() == '1' and message.from_user.username == admin_id:
				if message.from_user.username == 'andreyyalunin':
					print(message.chat.id)
					admin_channelId = message.chat.id
				markup = types.InlineKeyboardMarkup()
				btn_my_site= types.InlineKeyboardButton(text='To reserve')
				sheet_values=job()

				print(markup,"\n",btn_my_site,dir(btn_my_site))
				w=1

				for i in sheet_values:
					res = ""
					for z in i:
						x=0
						if res == "":
							res = z
						else:
							res = res + " " + z

						# if x==2:
						# 	if res in photos1:
						# 		idi=photos2[photos1.index(res)]


						# x +=1
					btn_my_site.callback_data = "{}".format(w)
					print(btn_my_site.callback_data,res)

					w += 1
					print("1",btn_my_site.callback_data)
					markup.add(btn_my_site)
					if w % 10 == 0:
					    time.sleep(7)


					for i in channels:
						# print("2",btn_my_site.callback_data)
						# bot.send_message(message.chat.id, 'https:/drive.google.com/file/d/{}/'.format(idi))
						a=bot.send_message(i, res, reply_markup = markup)
						channels[i].append(a.message_id)





					markup = types.InlineKeyboardMarkup()

				print(channels)



			if message.text.lower() == '2' and message.from_user.username == admin_id:
				for i in channels:
				    for z in channels[i]:
				        bot.delete_message(chat_id=i,message_id=z)



				    channels[i]=[]

				print(channels)







		@bot.callback_query_handler(func=lambda call: True)
		def query_handler(call):

			bot.forward_message(message.chat.id,message.chat.id, call.message.message_id)

			if type(call.data) == str:

				print(call.from_user.username)

				if call.data not in calldata:

					results = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
					 # Данные воспринимаются, как вводимые пользователем (считается значение формул)
					"valueInputOption": "USER_ENTERED",
					"data": [
						{"range": "Лист1!F{}".format(call.data),
						 "majorDimension": "ROWS",     # Сначала заполнять строки, затем столбцы
						 "values": [
									["".join(call.from_user.username)] # Заполняем первую строку
									  # Заполняем вторую строку
								   ]}
					]}).execute()


				else:
					ranges1 = ["Лист1!F{}".format(call.data)] #
					results1 = service.spreadsheets().values().batchGet(spreadsheetId = spreadsheetId,
														ranges = ranges1,
														valueRenderOption = 'FORMATTED_VALUE',
														dateTimeRenderOption = 'FORMATTED_STRING').execute()
					sheet_values = results1['valueRanges'][0]['values']
					print(sheet_values)
					sheet_values.append([call.from_user.username])
					strin=""
					for i in sheet_values:
						for q in i:
							strin = strin + q+" "
					results = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
					 # Данные воспринимаются, как вводимые пользователем (считается значение формул)
					"valueInputOption": "USER_ENTERED",
					"data": [
						{"range": "Лист1!F{}".format(call.data),
						 "majorDimension": "ROWS",     # Сначала заполнять строки, затем столбцы
						 "values": [
									["".join(strin)] # Заполняем первую строку
									  # Заполняем вторую строку
								   ]}
					]}).execute()


# 					value_range_body = {
# 					"range": "Лист1!F{}".format(call.data),
# 						 "majorDimension": "ROWS",     # Сначала заполнять строки, затем столбцы
# 						 "values": [
# 									[" ".join(call.from_user.username)] # Заполняем первую строку
# 									  # Заполняем вторую строку
# 								   ]
#     # TODO: Add desired entries to the request body.
# }



# 					request = service.spreadsheets().values().append(spreadsheetId=spreadsheetId, range=value_range_body["range"], valueInputOption="USER_ENTERED", insertDataOption="INSERT_ROWS", body=value_range_body)
# 					response = request.execute()
				calldata.append(call.data)
	else:
		bot.send_message(message.chat.id, 'Вашего юзернейм нет в списках. Обратитесь к администратору @telegram.')

def runBot():
	bot.polling()

def runSchedulers():
  schedule.every(60).seconds.do(job)

  while True:
      schedule.run_pending()
      time.sleep(1)

if __name__ == "__main__":
	t1 = threading.Thread(target=runBot)
	t2 = threading.Thread(target=runSchedulers)
	# starting thread 1
	t1.start()
	# starting thread 2
	t2.start()

