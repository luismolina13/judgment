#!/usr/bin/env python

import tornado.ioloop
import tornado.web
import os, uuid
 
__UPLOADS__ = "uploads/"

class MainHandler(tornado.web.RequestHandler):
    def get(self):
         self.write("Hello, world")
        #self.render("openID_login.html")

class UploadHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Upload a file with POST")

    def post(self):
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
    (r"/upload", UploadHandler),
])

if __name__ == "__main__":
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
