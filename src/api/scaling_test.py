import requests

url = "http://localhost:9000/get_number"
payload, headers = {}, {}

x = 0
while x < 100:
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    x += 1
