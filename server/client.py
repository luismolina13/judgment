import requests

url1='http://ec2-54-65-123-251.ap-northeast-1.compute.amazonaws.com/upload'

filehandle = open('./encryption')
r = requests.post(url1, data={},files = {'file':filehandle})
print r.status_code
print r.text
