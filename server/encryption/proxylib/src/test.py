from ctypes import cdll
lib = cdll.LoadLibrary('./proxylib_python.so')

class Foo(object):
    def __init__(self):
        self.obj = lib.Foo_new()

    def bar(self, s):
        lib.Foo_bar(self.obj, s)
    
    def generate_key(self, fname):
        lib.Foo_generate_key(self.obj, fname)

    def generate_reencrypt_key(self, pname, sname):
        lib.Foo_generate_reencrypt_key(self.obj, pname, sname)

    def encrypt(self, public_key, plain_text, file_name):
        lib.Foo_encrypt(self.obj, public_key, plain_text, file_name)

    def decrypt(self, secret_key, file_name):
        return lib.Foo_decrypt(self.obj, secret_key, file_name)

f = Foo()
f.bar("Luis") #and you will see "Hello" on the screen
f.generate_key("LuisKey")
f.generate_key("FriendKey")
f.generate_reencrypt_key("FriendKey_p", "LuisKey_s")
f.encrypt("LuisKey_p", "http://www.cplusplus.com/reference/cstring/strcpy/", "encryption")
print f.decrypt("LuisKey_s", "encryption")
