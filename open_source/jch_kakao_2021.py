import requests
import json

X_AUTH_TOKEN = '0786257bbb35fc49f4da077dbc04ec8b'
BASE_URL = 'https://kox947ka1a.execute-api.ap-northeast-2.amazonaws.com/prod/users'
ans1 = [5, 5, 4]
ans2 = [10, 60, 3]
prob = '1'

def start_api():
	headers = {
		'X-Auth-Token': X_AUTH_TOKEN,
		'Content-Type': 'application/json'
	}
	# data = '{"problem": ' + prob + '}'
	# response = requests.post(BASE_URL+'/start', headers=headers, data=data)
	data = {"problem": prob}
	response = requests.post(BASE_URL+'/start', headers=headers, data=json.dumps(data))
	print(response)
	
	Auth_data = response.json()
	Auth_key = Auth_data.get("auth_key")

	print(Auth_key)
	return Auth_key


def get_api(AUTH_KEY, link):
	headers = {
		'Authorization': AUTH_KEY,
		'Content-Type': 'application/json'
	}

	response = requests.get(BASE_URL+'/'+link, headers=headers)
	# print(response)

	Auth_data = response.json()
	info = Auth_data.get(link)
	Auth_json = json.dumps(info)
	# print(info)
	return info


def simulate_api(AUTH_KEY, command):
	headers = {
		'Authorization': AUTH_KEY,
		'Content-Type': 'application/json'
	}
	data = '{"commands": [' + command + '] }'
	# print(data)
	response = requests.put(BASE_URL+'/simulate', headers=headers, data=data)
	# print(response)

	Auth_data = response.json()
	print(Auth_data)
	status = Auth_data.get('status')

	# print(status)
	return status	

# 0: 6초간 아무것도 하지 않음
# 1: 위로 한 칸 이동
# 2: 오른쪽으로 한 칸 이동
# 3: 아래로 한 칸 이동
# 4: 왼쪽으로 한 칸 이동
# 5: 자전거 상차
# 6: 자전거 하차

def make_command2(ans):
	command = []
	for i in range(0, ans[0]):
		command.append('{ "truck_id": ' + str(i) + ', "command": [')
	return command

def algorithm(loc_info, truck_info, ans):
	command = make_command2(ans)
	for loc_t in truck_info:
		cur_loc = loc_t.get('location_id')
		id_t = loc_t.get('id')
		bike_c = loc_t.get('loaded_bikes_count')

		for i in range(0, 5):
			bike_num = loc_info[cur_loc].get('located_bikes_count')
			if bike_num >= 3:
				command[id_t] += '5, '
			elif bike_num == 0:
				command[id_t] += '6, '
			if loc_t.get('location_id') % ans[1] == ans[1]-1:
				command[id_t] += '3, '
				cur_loc -= 1
			else:
				command[id_t] += '1, '
				cur_loc += 1
		command[id_t] += '0] }'
	# print(', '.join(command))
	return ', '.join(command)

def make_command1(ans):
	command = ''
	for i in range(0, ans[0]):
		command += '{ "truck_id": ' + str(i) + ', "command": [' + '2, '*i +'0] }, '
	command = command[:-2]
	return command

AUTH_KEY = start_api()

status = 'ready'
if prob == '1':
	command = make_command1(ans1)
	print(command)
	while status == 'ready':
		status = simulate_api(AUTH_KEY,command)
		loc_info = get_api(AUTH_KEY, "locations")
		truck_info = get_api(AUTH_KEY, "trucks")
		command = algorithm(loc_info, truck_info, ans1)

else:
	command = make_command1(ans2)
	while status == 'ready':
		status = simulate_api(AUTH_KEY,command)
		loc_info = get_api(AUTH_KEY, "locations")
		truck_info = get_api(AUTH_KEY, "trucks")
		command = algorithm(loc_info, truck_info, ans2)
	
score_info = get_api(AUTH_KEY, "score")
print(score_info)
