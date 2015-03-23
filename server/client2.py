import csv
import requests
import threading
import time
import uuid
from proxylib import Proxylib

proxylib = Proxylib()
client_id = 0
server_url = 'http://ec2-54-65-123-251.ap-northeast-1.compute.amazonaws.com/'

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
    print 'Uploading file urls for' + client_id
    
    # Encrypt the file
    filename = str(uuid.uuid4())
    proxylib.encrypt('files/public_keys/' + str(client_id) + '_p', urls, filename)

    filehandle = open(filename)
    upload_url = server_url + 'upload/' + str(client_id)
    r = requests.post(server_url, data={},files = {'file':filehandle})
    print r.status_code
    print r.text
    # Delete the file
    os.remove(filename)

def download():
    print 'Downloading files'


def parse_history(history_file):
    urls = []
    with open(history_file, 'rb') as csvfile:
        historyreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in historyreader:
            urls.append(row[1])
    return urls

def main():
    url_threshold = 20
    current_urls = []
        
    urls = parse_history('luis_history.csv')

    @setInterval(1)
    def send_urls():
        if len(current_urls) < url_threshold:
            url = urls.pop(0).split('://')
            if len(url) > 1:
                if 'www.google' in url[1]:
                    pass
                else:
                    print url[1]
                    current_urls.append(url[1])
        else:
            # filename = str(uuid.uuid4()) + '.txt'
            # with open(filename, 'w') as fh:
            #     for url in current_urls:
            #         fh.write("%s\n" % url)
            upload('\n'.join(current_urls))
            del current_urls[:]

    @setInterval(5)
    def get_urls():



    send_urls()
    time.sleep(60)

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