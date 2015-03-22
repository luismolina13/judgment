from ctypes import cdll
lib = cdll.LoadLibrary('./encryption/proxylib/src/proxylib_python.so')

class Proxylib(object):
    def __init__(self):
        self.obj = lib.Proxylib_new()

    def bar(self, s):
        lib.Proxylib_bar(self.obj, s)
    
    def generate_key(self, fname):
        lib.Proxylib_generate_key(self.obj, fname)

    def generate_reencrypt_key(self, sname, pname, dname):
        lib.Proxylib_generate_reencrypt_key(self.obj, sname, pname, dname)

    def encrypt(self, public_key, plain_text, file_name):
        lib.Proxylib_encrypt(self.obj, public_key, plain_text, file_name)

    def reencrypt(self, del_key, enc_file_name, reenc_file_name):
        lib.Proxylib_reencrypt(self.obj, del_key, enc_file_name, reenc_file_name)
    
    def decrypt(self, secret_key, enc_file_name, dec_file_name):
        lib.Proxylib_decrypt(self.obj, secret_key, enc_file_name, dec_file_name)

# f = Proxylib()
# f.bar("Luis") #and you will see "Hello" on the screen
# f.generate_key("LuisKey")
# f.generate_key("FriendKey")
# f.generate_reencrypt_key("LuisKey_s", "FriendKey_p", "LuisKey_sFriendKey_p")
# f.encrypt("LuisKey_p", "http://www.cplusplus.com/reference/cstring/strcpy/", "encryption")
# f.reencrypt("LuisKey_sFriendKey_p", "encryption", "reencryption")
# f.decrypt("FriendKey_s", "reencryption", "decryption")
