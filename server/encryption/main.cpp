#include <iostream>

#include "proxylib_api.h"
#include "proxylib.h"
#include "proxylib_pre1.h"
#include "proxylib_pre2.h"

using namespace std;

int main() {
	char seedbuf[512];
	cout << initLibrary(); //seedbuf, 512) << endl;
	cout << "Hello" <<endl;
	return 0;
}
