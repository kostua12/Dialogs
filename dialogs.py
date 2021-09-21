import vk, time, os

os.system('clear')
banner = """\033[1m\033[32m
┏━━┳━━┳━━━━━┳━━━━━┳━━━━━┳━━━━━┳━━━━━┳━━━━━┳━━━━━┓
┃     ┃  ━━━┫  ━━━┫  ━━━┫  ━  ┃  ┏━━┫  ━━━┫  ━━━┫
┃ ┃ ┃ ┃  ━━━╋━━━  ┣━━━  ┃  ╻  ┃  ┗  ┃  ━━━╋━━━  ┃
┗━┻━┻━┻━━━━━┻━━━━━┻━━━━━┻━━┻━━┻━━━━━┻━━━━━┻━━━━━┛
\033[0m"""
print(banner)

file = open('tokens.txt', 'r')
tokens = file.readlines()
file.close()

for i in range(len(tokens)):
	token = tokens[i][:-1]
	if token == '':
		break
	try:
		profile = vk.API(vk.Session(access_token=token), v='5.89', lang='ru').users.get()[0]
		print("\033[1m\033[34m\033[7m " + str(i + 1) + " \033[32m " + profile['first_name'] + " " + profile['last_name'] + " \033[27m")
	except:
		print("\033[1m\033[34m\033[7m " + str(i + 1) + " \033[31m Invalid token \033[27m")

token = tokens[int(input("\n\033[1m\033[32mВведите номер аккаунта:\033[0m ")) - 1][:-1]
api = vk.API(vk.Session(access_token=token), v='5.89', lang='ru')
print()

while True:
	conversations = api.messages.getConversations()['items']

	i = 0
	user_ids = []
	while i < len(conversations):
		sender_peer = conversations[i]['conversation']['peer']
		if sender_peer['type'] == 'user':
			user_ids.append(sender_peer['id'])
			i += 1
		else:
			del(conversations[i])

	profiles = api.users.get(user_ids=user_ids)
	my_profile = api.users.get()[0]

	for i in range(len(conversations)):
		j = len(conversations) - i - 1
		conversation = conversations[j]
		profile = profiles[j]

		print("\033[1m\033[34m\033[7m " + str(j + 1) + " \033[32m " + profile['first_name'] + " " + profile['last_name'] + " \033[22m\033[27m")
		if len(conversation['last_message']['attachments']) > 0 and len(conversation['last_message']['text']) == 0:
			print("\033[31mВложение")
		else:
			print("\033[0m" + conversation['last_message']['text'])
		print("\033[0m")

	try:
		choice = int(input("\033[1m\033[32mВведите номер диалога:\033[0m ")) - 1
	except:
		print()
		break
	user_id = conversations[choice]['conversation']['peer']['id']
	user_name = "\033[1m\033[7m\033[32m " + profiles[choice]['first_name'] + " " + profiles[choice]['last_name'] + " \033[0m"
	my_name = "\033[1m\033[7m\033[34m " + my_profile['first_name'] + " " + my_profile['last_name'] + " \033[0m"

	i = 0
	messages = []
	while True:
		history = api.messages.getHistory(user_id=user_id, rev=1, count=200, offset=200*i)
		i += 1
		messages += history['items']

		if history['count'] != 200:
			break

		time.sleep(0.25)

	for message in messages:
		print()
		if message['from_id'] == user_id:
			print(user_name + "\033[37m " + time.strftime("%m/%d/%Y %H:%M:%S", time.localtime(message['date'])) + "\033[0m")
		else:
			print(my_name + "\033[37m " + time.strftime("%m/%d/%Y %H:%M:%S", time.localtime(message['date'])) + "\033[0m")
		print(message['text'])
		print("\033[31m" + str(message['attachments']))

		input()
	print("\033[1m\033[32mНажмите Enter для возврата к списку диалогов\033[0m")
	input()
