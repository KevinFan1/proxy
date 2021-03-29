import requests

ip = '157.90.199.133:1080'

url = 'http://httpbin.org/get'
proxies = {
    'http': 'http://' + ip,
    'https': 'https://' + ip,
}
response = requests.get(url, proxies=proxies)
print(response.headers)
print(response.cookies)
print(response.text)
