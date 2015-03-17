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

    def reencrypt(self, del_key, enc_file_name, reenc_file_name):
        lib.Foo_reencrypt(self.obj, del_key, enc_file_name, reenc_file_name)
    
    def decrypt(self, secret_key, enc_file_name, dec_file_name):
        lib.Foo_decrypt(self.obj, secret_key, enc_file_name, dec_file_name)

f = Foo()
f.bar("Luis") #and you will see "Hello" on the screen
f.generate_key("LuisKey")
f.generate_key("FriendKey")
f.generate_reencrypt_key("FriendKey_p", "LuisKey_s")
f.encrypt("LuisKey_p", "http://www.cplusplus.com/reference/cstring/strcpy/", "encryption")
f.reencrypt("LuisKey_sFriendKey_p", "encryption", "reencryption")
f.decrypt("FriendKey_s", "reencryption", "decryption")
