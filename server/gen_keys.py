from proxylib import Proxylib

proxylib = Proxylib()

for i in range(0, 100):
    proxylib.generate_key("files/public_keys/" + str(i))

