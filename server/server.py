#!/usr/bin/env python

import tornado.ioloop
import tornado.web
import os, uuid
from proxylib import Proxylib
import zipfile
import time
import datetime
 
__UPLOADS__ = "uploads/"
__DOWNLOADS__ = "downloads/"
__FILES__ = "files/"
__DEL_KEYS__ = "del_keys/"
proxylib = Proxylib()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
         self.write("Hello, world")
        #self.render("openID_login.html")

class UploadHandler(tornado.web.RequestHandler):
    def get(self, user_id):
        self.write("Upload a file with POST for user: %s" %user_id)

    def post(self, user_id):
        fileinfo = self.request.files['file'][0]
        #print "fileinfo is", fileinfo
        fname = fileinfo['filename']
        extn = os.path.splitext(fname)[1]
        fname += extn
        directory = __FILES__ + user_id + "/" + __UPLOADS__
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(directory + fname, 'w') as fh:
            fh.write(fileinfo['body'])
        fh.close()

        # Reencrypt the file I just received
        re_encrypt_start = time.time()
        del_key_dir = __FILES__ + user_id + "/" + __DEL_KEYS__
        for del_key in os.listdir(del_key_dir):
            friend_id = del_key.split('_')[1][1:]
            #print "friend_id:", friend_id
            download_directory = __FILES__ + friend_id + "/" + __DOWNLOADS__
            if not os.path.exists(download_directory):
                os.makedirs(download_directory)
            proxylib.reencrypt(str(del_key_dir + del_key), str(directory+fname), str(download_directory + fname))
        os.remove(str(directory + fname))
        #t = datetime.datetime.fromtimestamp(re_encrypt_start).strftime('%Y-%m-%d %H:%M:%S')
        t = time.time() - re_encrypt_start
        print "Seconds for re-encryption:", t
        #proxylib.decrypt("FriendKey_s", "reencryption_file", "decryption")

        # TODO send to all the friends or store somewhere to be used
        self.finish(fname + " is uploaded!! Check %s folder" %__UPLOADS__)

class DownloadHandler(tornado.web.RequestHandler):
    '''Creates a .zip file that contains the downloads folder with all the
       files inside of it.'''
    def get(self, user_id):
        files_dir = __FILES__ + user_id + '/'
        buf_size = 4096
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'attachment; filename=downloads.zip')

        os.chdir(files_dir)
        
        zip_dir = str(files_dir + 'downloads.zip')
        zipf = zipfile.ZipFile('downloads.zip', 'a')
        if not os.listdir('downloads/'):
            # No content status 204
            self.set_status(204)
            self.finish()
            os.chdir('../..')
            return
        for files in os.listdir('downloads/'):
            print os.getcwd()
            zipf.write(str('downloads/' + files))
        zipf.close()
        
        file_name = 'downloads.zip'
        with open(file_name, 'r') as f:
            while True:
                data = f.read(buf_size)
                if not data:
                    break
                self.write(data)
        os.remove('downloads.zip')
        os.chdir('../..')
        self.finish()

    def post(self, user_id):
        fileinfo = self.request.files['file'][0]
        print "fileinfo is", fileinfo
        fname = fileinfo['filename']
        extn = os.path.splitext(fname)[1]
        cname = str(uuid.uuid4()) + extn
        fh = open(__UPLOADS__ + cname, 'w')
        fh.write(fileinfo['body'])
        self.finish(cname + " is uploaded!! Check %s folder" %__UPLOADS__)

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/upload/([^/]+)", UploadHandler),
    (r"/download/([^/]+)", DownloadHandler),
])

if __name__ == "__main__":
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
