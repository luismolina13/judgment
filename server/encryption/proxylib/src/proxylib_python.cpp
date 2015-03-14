#include <iostream>
#include "proxylib_api.h"
#include "proxylib.h"
#include "proxylib_pre1.h"
#include "proxylib_pre2.h"
#include <string>
#include <algorithm>
#include <stdexcept>
extern Miracl precision;
 
#include <iostream>
#include <fstream>

using namespace std;

class Foo{
	std::string string_to_hex(const std::string& input)
	{
	    static const char* const lut = "0123456789ABCDEF";
	    size_t len = input.length();

	    std::string output;
	    output.reserve(2 * len);
	    for (size_t i = 0; i < len; ++i)
	    {
		const unsigned char c = input[i];
		output.push_back(lut[c >> 4]);
		output.push_back(lut[c & 15]);
	    }
	    return output;
	}

	std::string hex_to_string(const std::string& input)
	{
	    static const char* const lut = "0123456789ABCDEF";
	    size_t len = input.length();
	    if (len & 1) throw std::invalid_argument("odd length");

	    std::string output;
	    output.reserve(len / 2);
	    for (size_t i = 0; i < len; i += 2)
	    {
		char a = input[i];
		const char* p = std::lower_bound(lut, lut + 16, a);
		if (*p != a) throw std::invalid_argument("not a hex digit");

		char b = input[i + 1];
		const char* q = std::lower_bound(lut, lut + 16, b);
		if (*q != b) throw std::invalid_argument("not a hex digit");

		output.push_back(((p - lut) << 4) | (q - lut));
	    }
	    return output;
	}


	CurveParams gParams;
    public:
	Foo() {
		//cout << "HELLO WORLD" << endl;
		cout << string_to_hex("Hello World!") << endl;
		if (initLibrary() == FALSE) {
			cout << " ... FAILED" << endl;
		} else {
			cout << " ... OK" << endl;
		}

		//
		// Parameter generation test
		//
		cout << ". Generating curve parameters";
		if (PRE1_generate_params(gParams) == FALSE) {
			cout << " ... FAILED" << endl;
		} else {
			cout << " ... OK" << endl;
		}


	}
        void bar(char* str) {
            std::cout << "Hello " << std::endl;
            printf("%s\n", str);
        }

	void generate_key(char* file_name) {
          cout << ". Generating keypair 1";

          ProxyPK_PRE1 pk1;
          ProxySK_PRE1 sk1;
          if (PRE1_keygen(gParams, pk1, sk1) == FALSE) {
            cout << " ... FAILED" << endl;
          } else {
            //cout << "\nBinary size: " << pk1.getSerializedSize(SERIALIZE_BINARY) << endl;
            char buffer[1000];
            string secret_file(file_name);
            secret_file += "_s";
            string public_file(file_name);
            public_file += "_p";

            int pSize = pk1.serialize(SERIALIZE_BINARY, buffer, 1000);
            //cout << pSize << endl;
            ofstream pfile(public_file.c_str(), ios::binary | ios::out);
            pfile << pSize << '\n';
            pfile.write(buffer, pSize);
            pfile.close();
            //for (int i = 0; i < pSize; i++)           
            //    cout << (int)buffer[i] << ' ';            
            //pk1.serialize(SERIALIZE_HEXASCII, buffer, 1000);
            //printf("\n%s\n", buffer);

            int sSize = sk1.serialize(SERIALIZE_BINARY, buffer, 1000);
            ofstream sfile(secret_file.c_str(), ios::binary | ios::out);
            sfile << sSize << '\n';
            sfile.write(buffer, sSize);
            sfile.close();
            sk1.serialize(SERIALIZE_HEXASCII, buffer, 1000);
            printf("\n%s\n", buffer);
            cout << "\n ... OK" << endl;
          }
	}

        void generate_reencrypt_key(char* pname, char* sname) {
            char buffer[1000];
            ProxyPK_PRE1 pk;
            ifstream pfile(pname, ios::binary | ios::in);
            int pSize = 0;
            pfile >> pSize;
            cout << "Reencrypt: " << pSize << endl;
            char junk[1];
            pfile.read(junk, 1);
            pfile.read(buffer, pSize);
            pfile.close();
            //for (int i = 0; i < pSize; i++)  
            //    cout << (int)buffer[i] << ' ';
            pk.deserialize(SERIALIZE_BINARY, buffer, pSize);
            //pk.serialize(SERIALIZE_HEXASCII, buffer, 1000);
            //printf("\n%s\n", buffer);

            ProxySK_PRE1 sk;
            
            ifstream sfile(sname, ios::binary | ios::in);
            int sSize = 0;
            sfile >> sSize;
            cout << "Reencrypt Secret: " << sSize << endl;
            sfile.read(junk, 1);
            sfile.read(buffer, sSize);
            sfile.close();
            sk.deserialize(SERIALIZE_BINARY, buffer, sSize);
            sk.serialize(SERIALIZE_HEXASCII, buffer, 1000);
            printf("\n%s\n", buffer);

            ECn delKey;
            // Generate a delegation key from user1->user2
            if (PRE1_delegate(gParams, pk, sk, delKey) == FALSE) {
                cout << " ... FAILED" << endl;
            } else {
                cout << " ... OK" << endl;
            }
            string secret(sname);
            string publicF(pname);
            string rname = secret + publicF;
            int rSize = SerializeDelegationKey_PRE1(delKey, SERIALIZE_BINARY, buffer, 1000);
            ofstream rfile(rname.c_str(), ios::binary | ios::out);
            rfile << rSize << '\n';
            rfile.write(buffer, rSize);
            rfile.close();
            
        }
};

extern "C" {
    Foo* Foo_new(){ return new Foo(); }
    void Foo_bar(Foo* foo, char* str){ foo->bar(str); }
    void Foo_generate_key(Foo* foo, char* fname) { foo->generate_key(fname); }
    void Foo_generate_reencrypt_key(Foo* foo, char* pname, char* sname) { foo->generate_reencrypt_key(pname, sname); }
}


