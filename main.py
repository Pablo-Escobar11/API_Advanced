'''curl -X 'POST' \
  'http://5.63.153.31:5051/v1/account' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "login": "pasha_test",
  "email": "pasha_test@mail.ru",
  "password": "Xdvgy4321"
}'''
import pprint

import requests, json

# url = 'http://5.63.153.31:5051/v1/account'
#
# headers = {
#     'accept': '*/*',
#     'Content-Type': 'application/json'
# }
#
# payload = {
#     "login": "pasha_test2",
#     "email": "pasha2_test@mail.ru",
#     "password": "Xdvgy4321"
# }
#
# response = requests.post(url=url, headers=headers, json=payload)
#
# print(response.status_code)

url = 'http://5.63.153.31:5051/v1/account/212bcae0-64d3-457b-b885-c18d044ded03'

headers = {
    'accept': '*/*'
}

response = requests.put(url=url, headers=headers)

print(response.status_code)
pprint.pprint(response.json())
response_json = response.json()
print(response_json['resource']['rating']['quantity'])
