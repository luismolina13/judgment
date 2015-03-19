#!/usr/bin/env python

import tornado.ioloop
import tornado.web
import os, uuid
from proxylib import Proxylib
 
__UPLOADS__ = "uploads/"
#proxylib = Proxylib()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
         self.write("Hello, world")
        #self.render("openID_login.html")

class UploadHandler(tornado.web.RequestHandler):
    def get(self, user_id):
        self.write("Upload a file with POST for user: %s" %user_id)

    def post(self, user_id):
        fileinfo = self.request.files['file'][0]
        print "fileinfo is", fileinfo
        fname = fileinfo['filename']
        extn = os.path.splitext(fname)[1]
        fname += extn
        directory = __UPLOADS__ + user_id + "/"
        if not os.path.exists(directory):
            os.makedirs(directory)
        fh = open(directory + fname, 'w')
        fh.write(fileinfo['body'])

        # Reencrypt the file I just received
        proxylib = Proxylib()
        proxylib.reencrypt("LuisKey_sFriendKey_p", directory + fname, "reencryption_file")

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
