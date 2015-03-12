from ctypes import cdll
lib = cdll.LoadLibrary('./proxylib_python.so')

class Foo(object):
    def __init__(self):
        self.obj = lib.Foo_new()

    def bar(self, s):
        lib.Foo_bar(self.obj, s)
    
    def generate_key(self):
        lib.Foo_generate_key(self.obj)

f = Foo()
f.bar("Luis") #and you will see "Hello" on the screen
f.generate_key()
