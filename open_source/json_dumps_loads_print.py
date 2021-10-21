import json

user = {
	"id": 0,
	"username": "chjang",
	"password": "1234",
	"address": 'seoul',
	"nickname": ["ch", "cjang"]
}
print(user)
print(type(user))
# dumps - python->json
# read - json->python
json_data = json.dumps(user)
print(json_data)

print(type(json_data))
python_data = json.loads(json_data)
print(python_data)
print(type(python_data))

json_data2 = json.dumps(user, indent=4)
print(json_data2)
print(type(json_data2))
