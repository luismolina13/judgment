import requests
from tornado import httpclient
http_client = httpclient.HTTPClient()
url='http://ec2-54-92-44-89.ap-northeast-1.compute.amazonaws.com/download/1'
count = 1
try:
    response = http_client.fetch(url)
    with open("file" + str(count) + ".zip", 'w') as f:
	f.write(response.body)
	count += 1
except httpclient.HTTPError as e:
    print("Error:", e)
http_client.close()

#url1='http://ec2-54-92-44-89.ap-northeast-1.compute.amazonaws.com/upload/0'

#filehandle = open('./file1')
#r = requests.post(url1, data={},files = {'file':filehandle})
#print r.status_code
#print r.text
