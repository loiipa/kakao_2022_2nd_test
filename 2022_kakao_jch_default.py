import requests
import json

# 게임 매칭 알고리즘 설계하기
X_Auth_Token = '496c5cad4fb961dc4f0684dac3b119a3'
BASE_URL = 'https://huqeyhi95c.execute-api.ap-northeast-2.amazonaws.com/prod'
limit_time = 0
grade_change = 0.001

def start_api(prob):
	headers = {
		'X-Auth-Token': X_Auth_Token,
		'Content-Type': 'application/json'
	}
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
	if link == 'score':
		return Auth_data
	else:
		info = Auth_data.get(link)
		# print(info)
		return info

def put_api(AUTH_KEY, link, value):
	headers = {
		'Authorization': AUTH_KEY,
		'Content-Type': 'application/json'
	}
	if link == 'match':
		data = {"pairs": value}
	elif link == 'change_grade':
		data = {"commands": value}

	response = requests.put(BASE_URL+'/'+link, headers=headers, data=json.dumps(data))
	# print(response)

	Auth_data = response.json()
	# info = Auth_data.get(link)
	# print(info)
	if link == 'match':
		print(Auth_data)
	return Auth_data

def init_grade(user_num, avg):
	commands = []
	for i in range(1, user_num+1):
		commands.append({"id": i, "grade": avg})
	change_grade = put_api(Auth_key, 'change_grade', commands)

def match_algorithm(Auth_key):
	waiting_line = get_api(Auth_key, 'waiting_line')
	user_info = get_api(Auth_key, 'user_info')
	waiting_list = []
	pairs = []
	for val in waiting_line:
		grade = user_info[int(val.get('id')) - 1].get('grade')
		waiting_list.append([grade, val.get('id'), val.get('from')])
	waiting_list = sorted(waiting_list)
	l_len = len(waiting_list) - 1
	if l_len > 0:
		for i in range(0, l_len, 2):
			pairs.append([waiting_list[i][1], waiting_list[i+1][1]])
	# print(pairs)
	return pairs
	
def grade_algorithm(Auth_key):
	# 등급의 범위가 0~9999를 넘어가는 예외도 처리해야 할 듯
	game_result = get_api(Auth_key, 'game_result')
	user_info = get_api(Auth_key, 'user_info')
	commands = []
	for res in game_result:
		grade_fix = 41 - res.get('taken')

		winner = res.get('win')
		grade = user_info[winner - 1].get('grade')
		commands.append({"id": winner, "grade": grade + grade_fix})

		loser = res.get('lose')
		grade = user_info[loser - 1].get('grade')
		commands.append({"id": loser, "grade": grade - grade_fix})
	change_grade = put_api(Auth_key, 'change_grade', commands)

# 들어오는대로 매칭 하는 것 ->default
# 일정시간 대기 후 제일 비슷한 사람 매칭 ->개선방법?
# 이 둘 사이의 줄다리기일 듯?

# 실력의 평균 = 40000 -> 일괄 40000을 주는 것부터 시작?
# 걸린시간->실력차이 확인. 등급 상승이나 하락에 대한 퍼센트는 20%?
# 3이거나 40인 경우는 10% 조절
# waiting list는 항상 정렬상태
# 특정 인원 이상인 경우 매칭 할 수 있도록
# 특정 시간 이상인 경우 강제 매칭
# 등급 상승에 대한 알고리즘

# waiting_line = get_api(Auth_key, 'waiting_line')
# { "id": 1, "from": 3 }

# game_result = get_api(Auth_key, 'game_result')
# {"win": 10, "lose": 2, "taken": 7 }

# user_info = get_api(Auth_key, 'user_info')
# { "id": 1, "grade": 2100 }

# match = put_api(Auth_key, 'match')					data = {"pairs": [[1, 2], [9, 7], [11, 49]]}
# {"status": "ready", "time": 312}

# change_grade = put_api(Auth_key, 'change_grade')		data = {"commands": [{ "id": 1, "grade": 1900 }]}
# {"status": "ready"}

######################################################
Auth_key = start_api('1')
status = 'ready'
pairs = []
init_grade(30, 5000)
while status == 'ready':
	pairs = match_algorithm(Auth_key)
	match = put_api(Auth_key, 'match', pairs)
	status = match.get('status')
	grade_algorithm(Auth_key)
	if match.get('time') % 10 == 0:
		print(pairs)

# for _ in range(5):
# 	match = put_api(Auth_key, 'match', pairs)
# match_algorithm(Auth_key)

# 게임 끝난 뒤 반환됨
score = get_api(Auth_key, 'score')
print(score)
######################################################
######################################################
Auth_key = start_api('2')
status = 'ready'
pairs = []
init_grade(900, 5000)
while status == 'ready':
	pairs = match_algorithm(Auth_key)
	match = put_api(Auth_key, 'match', pairs)
	status = match.get('status')
	grade_algorithm(Auth_key)
	if match.get('time') % 10 == 0:
		print(pairs)
score = get_api(Auth_key, 'score')
print(score)
######################################################
# {'status': 'finished', 'efficiency_score': '99.899', 
# 'accuracy_score1': '65.1111', 'accuracy_score2': '51.037', 
# 'score': '219.2969'}
# {'status': 'finished', 'efficiency_score': '99.8774', 
# 'accuracy_score1': '19.2449', 'accuracy_score2': '64.3758', 
# 'score': '180.2468'}
