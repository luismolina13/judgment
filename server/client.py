import csv
import os
import requests
import shutil
import threading
import time
import uuid
import zipfile
from proxylib import Proxylib

url_threshold = 1
proxylib = Proxylib()

client_id = 0
# Lisa's Server
# server_url = 'http://ec2-54-92-44-89.ap-northeast-1.compute.amazonaws.com/'
# Luis' Server
server_url = 'http://ec2-52-68-29-226.ap-northeast-1.compute.amazonaws.com/'

def setInterval(interval, times = -1):
    # This will be the actual decorator,
    # with fixed interval and times parameter
    def outer_wrap(function):
        # This will be the function to be
        # called
        def wrap(*args, **kwargs):
            stop = threading.Event()

            # This is another function to be executed
            # in a different thread to simulate setInterval
            def inner_wrap():
                i = 0
                while i != times and not stop.isSet():
                    stop.wait(interval)
                    function(*args, **kwargs)
                    i += 1

            t = threading.Timer(0, inner_wrap)
            t.daemon = True
            t.start()
            return stop
        return wrap
    return outer_wrap

def upload(urls):
    print 'Uploading urls for client ' + str(client_id)
    
    # Encrypt the file
    filename = str(uuid.uuid4())
    proxylib.encrypt('files/public_keys/' + str(client_id) + '_p', urls, filename)

    filehandle = open(filename)
    upload_url = server_url + 'upload/' + str(client_id)
    r = requests.post(upload_url, data={},files = {'file':filehandle})
    print r.status_code
    print r.text
    # Delete the file
    os.remove(filename)

def download():
    print 'Downloading files'
    download_url = server_url + 'download/' + str(client_id)
    r = requests.get(download_url)
    if r.status_code == 204:
        return None

    filename = str(uuid.uuid4())
    with open(filename + '.zip', 'w') as f:
        f.write(r.content)

    return filename
    # try:
    #     response = http_client.fetch(url)
    #     with open("file" + str(count) + ".zip", 'w') as f:
    #     f.write(response.body)
    #     count += 1
    # except httpclient.HTTPError as e:
    #     print("Error:", e)
    # http_client.close()


def parse_history(history_file):
    urls = []
    with open(history_file, 'rb') as csvfile:
        historyreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in historyreader:
            urls.append(row[1])
    return urls

def main():
    friends_urls = []

    urls = parse_history('luis_history.csv')
    
    @setInterval(1)
    def send_urls():
        if len(urls) == 0:
            return
        url = urls.pop(0).split('://')
        if len(url) > 1:
            if 'www.google' in url[1]:
                pass
            else:
                if len(url[1]) > 132:
                    # TODO: convert to tiny url
                    url[1] = url[1][0:132]
                print "============> ", url[1], len(url[1])
                upload(url[1])

    @setInterval(5)
    def get_urls():
        filename = download()
        if not filename:
            return
        zipf = zipfile.ZipFile(filename + '.zip')
        zipf.extractall(filename)
        for file_name in os.listdir(filename + '/downloads/'):
            decrypted_file = str(uuid.uuid4())
            proxylib.decrypt('files/public_keys/' + str(client_id) + '_s', filename + '/downloads/' + file_name, filename + '/' + decrypted_file)
            with open(filename + '/' + decrypted_file, 'r') as df:
                dec_urls = df.readlines()
                for dec_url in dec_urls:
                    print "Decrypted Urls: ", dec_url
                #friends_urls += dec_urls
        shutil.rmtree(filename)
        os.remove(filename + '.zip')

    send_urls()
    get_urls()
    time.sleep(100)

    # @setInterval(1)
    # def foo(a):
    #     print(a)

    # foo('bar')
    # time.sleep(5)
    # Will print 'bar' 3 times with 1 second delays

    # time.sleep(5)
    # stopper.set()
    # It will stop here, after printing 'bar' 5 times.
    # while True:
    #     time.sleep(1)
    #     print count
    #     count += 1


if __name__ == "__main__":
    main()
