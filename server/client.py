import bitly_api
import csv
import datetime
import operator
import os
import requests
import shutil
import threading
import time
import tinyurl
import urllib2
import uuid
import zipfile


from proxylib import Proxylib
from random import randint

BITLY_ACCESS_TOKEN = "84b5098ee1dc11ffe4d23e0999846c62c84a49bd"
url_threshold = 1
proxylib = Proxylib()

# Lisa's Server
#server_url = 'http://ec2-54-178-192-75.ap-northeast-1.compute.amazonaws.com/'
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

def upload(urls, encr_stats, upld_stats):
    client_id = randint(0,99)
    print 'Uploading urls for client ' + str(client_id)
    # Encrypt the file
    filename = str(uuid.uuid4())

    encr_begin = time.time()
    proxylib.encrypt('files/public_keys/' + str(client_id) + '_p', str(urls), filename)
    encr_time = time.time() - encr_begin
    print encr_stats['avg']
    encr_stats['avg'] += encr_time
    encr_stats['count'] += 1
    if encr_time < encr_stats['min']:
        encr_stats['min'] = encr_time
    if encr_time > encr_stats['max']:
        encr_stats['max'] = encr_time

    filehandle = open(filename)
    upload_url = server_url + 'upload/' + str(client_id)
    upload_begin = time.time()
    r = requests.post(upload_url, data={},files = {'file':filehandle})
    print r.status_code
    upload_time = time.time() - upload_begin
    print upld_stats['avg']
    upld_stats['avg'] += upload_time
    upld_stats['count'] += 1
    if upload_time < upld_stats['min']:
        upld_stats['min'] = upload_time
    if upload_time > upld_stats['max']:
        upld_stats['max'] = upload_time
    print r.text
    # Delete the file
    os.remove(filename)

def download(down_stats, client_id):
    print 'Downloading files'
    download_url = server_url + 'download/' + str(client_id)
    download_begin = time.time()
    r = requests.get(download_url)
    if r.status_code == 204:
        return None

    filename = str(uuid.uuid4())
    with open(filename + '.zip', 'w') as f:
        f.write(r.content)

    download_time = time.time() - download_begin
    print down_stats['avg']
    down_stats['avg'] += download_time
    down_stats['count'] += 1
    if download_time < down_stats['min']:
        down_stats['min'] = download_time
    if download_time > down_stats['max']:
        down_stats['max'] = download_time

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

def print_url_stats(friends_urls, most_recent, resolve_urls=False):
    print "########## Most Recent Urls ##########"
    for url in most_recent:
        if resolve_urls:
            try:
                response = urllib2.urlopen(url)
                print response.url
            except urllib2.HTTPError as err:
                print err
                print url
        else:
            print url
    print "######################################"

    print "############ Top 10 Urls #############"
    sorted_by_count = sorted(friends_urls.items(), key=operator.itemgetter(1))
    sorted_by_count.reverse()
    length = 10
    if len(sorted_by_count) < 10:
        length = len(sorted_by_count)
    for num in range(0, length):
        if resolve_urls:
            try:
                response = urllib2.urlopen(sorted_by_count[num][0])
                print response.url, sorted_by_count[num][1]
            except urllib2.HTTPError as err:
                print err
                print sorted_by_count[num][0], sorted_by_count[num][1]
        else:
            print sorted_by_count[num]
    print "######################################"


def print_and_write(name, stats):
    avg = 0.0
    if stats['count']:
        avg = stats['avg'] / stats['count']
    else:
        stats['min'] = 0.0
    print name, "count:", stats['count']
    print name, "average:", avg
    print name, "min:", stats['min']
    print name, "max:", stats['max']
    filename = name + "_times.txt"
    with open(filename, 'a') as wfile:
        wfile.write("%d,%f,%f,%f\n" % (stats['count'], avg, stats['min'], stats['max']))

def main():
    friends_urls = {}
    most_recent = []

    urls = parse_history('luis_history.csv')
    #urls = []#'http://he11oworld.comhe11oworld.comhe11oworld.comhe11oworld.comhe11oworld.comhe11oworld.com']#, 'http://superuser.com/questions/can-chrome-browser-history-be-exported-to-an-html-file']

    # count, min, max, avg
    upld_stats = {'count': 0, 'min': 1.0, 'max': 0.0, 'avg': 0.0}
    encr_stats = {'count': 0, 'min': 1.0, 'max': 0.0, 'avg': 0.0}
    down_stats = {'count': 0, 'min': 1.0, 'max': 0.0, 'avg': 0.0}
    decr_stats = {'count': 0, 'min': 1.0, 'max': 0.0, 'avg': 0.0}
    # download file counts
    durl_stats = {'count': 0, 'min': 1000, 'max': 0, 'avg': 0.0}

    @setInterval(1)
    def send_urls():
        if len(urls) == 0:
            return        
        url_for_tiny = urls.pop(0)
        url = url_for_tiny.split("://")
        if len(url) > 1:
            if 'www.google' in url[1]:
                pass
            else:
                bitly = bitly_api.Connection(access_token=BITLY_ACCESS_TOKEN)
                data = bitly.shorten(url_for_tiny)
                print data
                tiny_url = data['url']
                if len(tiny_url) > 132:
                    # TODO: convert to tiny url
                    tiny_url = tiny_url[0:132]
                print "============> ", url[1], tiny_url, len(tiny_url)
                upload(tiny_url, encr_stats, upld_stats)

    @setInterval(5)
    def get_urls():
        client_id = randint(0,99)
        filename = download(down_stats, client_id)
        if not filename:
            return
        zipf = zipfile.ZipFile(filename + '.zip')
        zipf.extractall(filename)
        url_num = len(os.listdir(filename + '/downloads/'))
        print durl_stats['avg']
        durl_stats['avg'] += url_num
        durl_stats['count'] += 1
        if url_num < durl_stats['min']:
            durl_stats['min'] = url_num
        if url_num > durl_stats['max']:
            durl_stats['max'] = url_num
        
        decr_begin = time.time()
        for file_name in os.listdir(filename + '/downloads/'):
            decrypted_file = str(uuid.uuid4())
            proxylib.decrypt('files/public_keys/' + str(client_id) + '_s', filename + '/downloads/' + file_name, filename + '/' + decrypted_file)
            with open(filename + '/' + decrypted_file, 'r') as df:
                dec_urls = df.readlines()
                for dec_url in dec_urls:
                    #fp = urllib2.urlopen(dec_url)
                    print "<============ ", dec_url#, fp.geturl()
                    if dec_url in friends_urls:
                        friends_urls[dec_url] += 1
                    else:
                        friends_urls[dec_url] = 1
                    most_recent.insert(0, dec_url)
                    if len(most_recent) > 10:
                        most_recent.pop()
        decr_time = time.time() - decr_begin 
        print decr_stats['avg']
        decr_stats['avg'] += decr_time
        decr_stats['count'] += 1
        if decr_time < decr_stats['min']:
            decr_stats['min'] = decr_time
        if decr_time > decr_stats['max']:
            decr_stats['max'] = decr_time

        shutil.rmtree(filename)
        os.remove(filename + '.zip')

        # Print the top 10 urls and the 10 most recent
        print_url_stats(friends_urls, most_recent)

    send_urls()
    get_urls()
    time.sleep(16)
    
    print_and_write('Upload', upld_stats)
    print_and_write('Encryption', encr_stats)
    print_and_write('Download', down_stats)
    print_and_write('Decryption', decr_stats)
    print_and_write('Num_download_files', durl_stats)

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

    #print_url_stats(friends_urls, most_recent, True)

if __name__ == "__main__":
    main()
