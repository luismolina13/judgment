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

class Proxylib{
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

        void save_file(char* file_name, char* buffer, int size) {
            ofstream file(file_name, ios::binary | ios::out);
            file << size << '\n';
            file.write(buffer, size);
            file.close();
        }

        void read_file(char* file_name, char* &buffer, int& size) {
            ifstream file(file_name, ios::binary | ios::in);
            size = 0;
            file >> size;
            char junk[1];
            buffer = new char[size];
            file.read(junk, 1);
            file.read(buffer, size);
            file.close();
        }
        
        ProxyPK_PRE1 read_public_key(char* name) {
            ProxyPK_PRE1 pk;
            ifstream file(name, ios::binary | ios::in);
            int size = 0;
            file >> size;
            char junk[1];
            char* buffer = new char[size];
            file.read(junk, 1);
            file.read(buffer, size);
            file.close();
            pk.deserialize(SERIALIZE_BINARY, buffer, size);
            delete [] buffer;
            return pk;
        }

        ECn read_del_key(char* name) {
            ECn delKey;
            ifstream file(name, ios::binary | ios::in);
            int size = 0;
            file >> size;
            char junk[1];
            char* buffer = new char[size];
            file.read(junk, 1);
            file.read(buffer, size);
            file.close();
            DeserializeDelegationKey_PRE1(delKey, SERIALIZE_BINARY, buffer, size);
            delete [] buffer;
            return delKey;
        }

        ProxySK_PRE1 read_secret_key(char* name) {
            ProxySK_PRE1 sk;
            ifstream file(name, ios::binary | ios::in);
            int size = 0;
            file >> size;
            char junk[1];
            char* buffer = new char[size];
            file.read(junk, 1);
            file.read(buffer, size);
            file.close();
            sk.deserialize(SERIALIZE_BINARY, buffer, size);
            delete [] buffer;
            return sk;
        }


	CurveParams gParams;
    public:
	Proxylib() {
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
        ifstream file("GenParam", ios::binary | ios::in);
        if(file) {
            /*if (PRE1_generate_params(gParams) == FALSE) {
                cout << "Nope. Doesn't work." << endl;
            } else {
                cout << "Maybe it worked?" << endl;
            }*/
            // Read parameters
            int size = 0;
            char junk[1];

            file >> size;
            file.read(junk, 1);

            char* buffer = new char[size];
            file.read(buffer, size);    

            file.close();
            gParams.deserialize(SERIALIZE_BINARY, buffer, size);
            
            cout << "P after: " << gParams.P << endl;

            delete [] buffer;
        }
        else {
            // Generate parameters
            cout << ". Generating curve parameters";
    		if (PRE1_generate_params(gParams) == FALSE) {
    			cout << " ... FAILED" << endl;
    		} else {
    			cout << " ... OK" << endl;
    		}

            // Save parameters
            ofstream file("GenParam", ios::binary | ios::out);
            int size = gParams.getSerializedSize(SERIALIZE_BINARY);
            char* buffer = new char[1000];
            
            cout << "bits_local: " << gParams.bits_local << endl;
            cout << "P: " << gParams.P << endl;
            
            size = gParams.serialize(SERIALIZE_BINARY, buffer, 1000);
            
            //CurveParams newParams;
            //newParams.deserialize(SERIALIZE_BINARY, buffer, size);
            //cout << "equal? " << (gParams == newParams);
            //cout << "P: " << newParams.P << endl;
            file << size << '\n';
            file.write(buffer, size);
            file.close();

            /*ifstream file2("GenParam", ios::binary | ios::in);
            char junk[1];

            file2 >> size;
            file2.read(junk, 1);

            char* buffer2 = new char[size];
            file2.read(buffer2, size);

            file2.close();
            CurveParams newParam;
            newParam.deserialize(SERIALIZE_BINARY, buffer2, size);
            cout << "equal? " << (gParams == newParam);
            delete [] buffer;
            */
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
            pk1.serialize(SERIALIZE_HEXASCII, buffer, 1000);
            printf("\n%s\n", buffer);

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
            ProxyPK_PRE1 pk = read_public_key(pname);
            ProxySK_PRE1 sk = read_secret_key(sname);
            
            sk.serialize(SERIALIZE_HEXASCII, buffer, 1000);
            printf("\n%s\n", buffer);
            pk.serialize(SERIALIZE_HEXASCII, buffer, 1000);
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

        void save_ciphertext(ProxyCiphertext_PRE1 ciphertext, char* file_name) {
            int size = ciphertext.getSerializedSize(SERIALIZE_BINARY);
            char* buffer = new char[size*2];
            int size2 = ciphertext.serialize(SERIALIZE_BINARY, buffer, size*2);
            //for (int i = 0; i < size2; i++)           
            //    cout << (int)buffer[i] << ' ';            
            save_file(file_name, buffer, size2);
            delete [] buffer;
        }

        void encrypt(char* public_key, char* plain_text, char* file_name) {
            cout << "...Start encryption" << endl;
            miracl *mip=&precision;
            Big plaintext;
            string plaintext_hex = string_to_hex(string(plain_text));
            char* text = new char[plaintext_hex.size() + 1];
            strncpy(text, plaintext_hex.c_str(), plaintext_hex.size() + 1);
            mip->IOBASE = 16;
            plaintext = text;

            ProxyPK_PRE1 pk = read_public_key(public_key);

            ProxyCiphertext_PRE1 ciphertext;
            if (PRE1_level2_encrypt(gParams, plaintext, pk, ciphertext) == FALSE) {
                cout << " ... FAILED ENCRYPTION" << endl;
            } else {
                // Save the ciphertext
                save_ciphertext(ciphertext, file_name);
            }
            cout << "...Finish encryption" << endl; 
        }

        ProxyCiphertext_PRE1 read_ciphertext(char* file_name) {
            ProxyCiphertext_PRE1 ciphertext;
            char* buffer;
            int size;
            read_file(file_name, buffer, size);
            cout << size << endl;
            //for (int i = 0; i < size; i++)           
            //    cout << (int)buffer[i] << ' ';            
            ciphertext.deserialize(SERIALIZE_BINARY, buffer, size);
            delete [] buffer;
            return ciphertext;
        }

        void reencrypt(char* del_key, char* enc_file_name, char* reenc_file_name) {
            cout << "...Start reencryption" << endl;
            // Re-encryption/decryption test
            ProxyCiphertext_PRE1 ciphertext = read_ciphertext(enc_file_name);
            ProxyCiphertext_PRE1 newCiphertext;
            ECn delKey = read_del_key(del_key);
            // Re-encrypt ciphertext from user1->user2 using delKey
            // We make use of the ciphertext generated in the previous test.
            if (PRE1_reencrypt(gParams, ciphertext, delKey, newCiphertext) == FALSE) {
                cout << " ... FAILED1" << endl;
            } else {
                save_ciphertext(newCiphertext, reenc_file_name);
            }
            cout << "...Finish reencryption" << endl;
        }

        void decrypt(char* secret_key, char* enc_file_name, char* dec_file_name) {
            cout << "...Start decryption" << endl;
            ProxySK_PRE1 sk = read_secret_key(secret_key);
            miracl *mip=&precision;
            Big plaintext = 0;

            ProxyCiphertext_PRE1 ciphertext = read_ciphertext(enc_file_name);

            // Decrypt the ciphertext
            if (PRE1_decrypt(gParams, ciphertext, sk, plaintext) == FALSE) {
                cout << " ... FAILED" << endl;
            } else {
                cout << " ... OK" << endl;
                mip->IOBASE=16;
                int size = ciphertext.getSerializedSize(SERIALIZE_BINARY);
                char* c2 = new char[size*2];
                c2 << plaintext;
                string result(c2);
                cout << hex_to_string(result) << endl;
                ofstream dec_file(dec_file_name);
                dec_file << hex_to_string(result);
                dec_file.close();
                printf("\n%s\n", c2);
                delete [] c2;
            }
            cout << "...Finish decryption" << endl;
        }
};

extern "C" {
    Proxylib* Proxylib_new(){ return new Proxylib(); }
    void Proxylib_bar(Proxylib* proxylib, char* str){ proxylib->bar(str); }
    void Proxylib_generate_key(Proxylib* proxylib, char* fname) { proxylib->generate_key(fname); }
    void Proxylib_generate_reencrypt_key(Proxylib* proxylib, char* pname, char* sname) { proxylib->generate_reencrypt_key(pname, sname); }
    void Proxylib_encrypt(Proxylib* proxylib, char* public_key, char* plain_text, char* file_name) { proxylib->encrypt(public_key, plain_text, file_name); }
    void Proxylib_reencrypt(Proxylib* proxylib, char* del_key, char* enc_file_name, char* reenc_file_name) { proxylib->reencrypt(del_key, enc_file_name, reenc_file_name); }
    void Proxylib_decrypt(Proxylib* proxylib, char* secret_key, char* enc_file_name, char* dec_file_name) { proxylib->decrypt(secret_key, enc_file_name, dec_file_name); }
}


