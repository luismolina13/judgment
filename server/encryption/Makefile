
LIBB = /home/ubuntu/judgment/server/encryption
LIBINCLUDE = /home/ubuntu/judgment/server/encryption/proxylib/src
MINCLUDE = /home/ubuntu/judgment/server/encryption/miracl

CFLAGS += -I$(LIBINCLUDE) -I$(MINCLUDE)
LDFLAGS += -L$(LIBB)

LDFLAGS += -static -lproxylibmiracl

# g++ main.cpp -I/home/ubuntu/judgment/server/encryption/proxylib/src/ -L/home/ubuntu/judgment/server/encryption -lproxylibmiracl
main: main.cpp
	g++ $(CFLAGS) $(LDFLAGS) $< -o $@
