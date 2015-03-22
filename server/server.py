#!/usr/bin/env python

import tornado.ioloop
import tornado.web
import os, uuid
from proxylib import Proxylib
 
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
        #print directory + fname
        del_key_dir = __FILES__ + user_id + "/" + __DEL_KEYS__
        for del_key in os.listdir(del_key_dir):
            friend_id = del_key.split('_')[1][1:]
            #print "friend_id:", friend_id
            download_directory = __FILES__ + friend_id + "/" + __DOWNLOADS__
            if not os.path.exists(download_directory):
                os.makedirs(download_directory)
            proxylib.reencrypt(str(del_key_dir + del_key), str(directory+fname), str(download_directory + fname))
        #proxylib.decrypt("FriendKey_s", "reencryption_file", "decryption")

        # TODO send to all the friends or store somewhere to be used
        self.finish(fname + " is uploaded!! Check %s folder" %__UPLOADS__)

class DownloadHandler(tornado.web.RequestHandler):
    def get(self, user_id):
        self.write("Upload a file with POST for user: %s" %user_id)

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
