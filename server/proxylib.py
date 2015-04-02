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
#with open('100_node_links.txt', 'r') as fileInput:
#    for line in fileInput:
#        friends = line.split()
#        friend1p = "files/public_keys/" + str(friends[0]) + "_p"
#        friend1s = "files/public_keys/" + str(friends[0]) + "_s"
#        friend2p = "files/public_keys/" + str(friends[1]) + "_p"
#        friend2s = "files/public_keys/" + str(friends[1]) + "_s"
#        print "friend1p:", friend1p
#        print "friend1s:", friend1s
#        print "friend2p:", friend2p
#        print "friend2s:", friend2s
#        friend1_sfriend2_p = "files/"+str(friends[0])+"/del_keys/"+str(friends[0])+"_s"+str(friends[1])+"_p"
#        friend2_sfriend1_p = "files/"+str(friends[1])+"/del_keys/"+str(friends[1])+"_s"+str(friends[0])+"_p"
#        print "friend1_sfriend2_p:", friend1_sfriend2_p
#        print "friend2_sfriend1_p:", friend2_sfriend1_p 
#        f.generate_reencrypt_key(friend1s, friend2p, friend1_sfriend2_p)
#        f.generate_reencrypt_key(friend2s, friend1p, friend2_sfriend1_p)

