#include <iostream>
#include "proxylib_api.h"
#include "proxylib.h"
#include "proxylib_pre1.h"
#include "proxylib_pre2.h"

using namespace std;

int testNum = 0, testsSuccess = 0;

int main() {
	cout << "HELLO WORLD" << endl;
	if (initLibrary() == FALSE) {
    		cout << " ... FAILED" << endl;
  	} else {
    		cout << " ... OK" << endl;
    		//testsSuccess++;
  	}

  // ******
  // PRE1 Tests
  // ******

  cout << endl << "TESTING PRE1 ROUTINES" << endl << endl;

  CurveParams gParams;
  //
  // Parameter generation test
  //
  cout << ". Generating curve parameters";
  if (PRE1_generate_params(gParams) == FALSE) {
    cout << " ... FAILED" << endl;
  } else {
    cout << " ... OK" << endl;
    testsSuccess++;
  }

  //
  // Key generation tests
  //
  cout << ++testNum << ". Generating keypair 1";
  ProxyPK_PRE1 pk1;
  ProxySK_PRE1 sk1;
  if (PRE1_keygen(gParams, pk1, sk1) == FALSE) {
    cout << " ... FAILED" << endl;
  } else {
    cout << " ... OK" << endl;
    testsSuccess++;
  }

  cout << ++testNum << ". Generating keypair 2";
  ProxyPK_PRE1 pk2;
  ProxySK_PRE1 sk2;
  if (PRE1_keygen(gParams, pk2, sk2) == FALSE) {
    cout << " ... FAILED" << endl;
  } else {
    cout << " ... OK" << endl;
    testsSuccess++;
  }
}

/*
#include <iostream>
#include <fstream>
#include <cstring>
#include <sys/time.h>

using namespace std;

#ifdef BENCHMARKING
	#include "benchmark.h"
#endif
#include "proxylib_api.h"
#include "proxylib.h"
#include "proxylib_pre1.h"
#include "proxylib_pre2.h"

#ifdef BENCHMARKING
static struct timeval gTstart, gTend;
static struct timezone gTz;
extern Benchmark gBenchmark;
#endif

#include <iostream>
#include <fstream>
#include <cstring>
#include <sys/time.h>

using namespace std;

#include "proxylib.h"
#include "proxylib_pre1.h"

#define NUMENCRYPTIONS 100

static CurveParams gParams;
int testNum = 0, testsSuccess = 0;

#ifdef BENCHMARKING
Benchmark gBenchmark(NUMBENCHMARKS);
#endif

//
// Main routine for tests
//

int main()
{
  cout << "Proxy Re-encryption Library" << endl << "Diagnostic Test Routines" << endl
       << endl;

  //
  // Initialize library test
  //
  cout << ++testNum << ". Initializing library";
  if (initLibrary() == FALSE) {
    cout << " ... FAILED" << endl;
  } else {
    cout << " ... OK" << endl;
    testsSuccess++;
  }

  // ******
  // PRE1 Tests
  // ******

  cout << endl << "TESTING PRE1 ROUTINES" << endl << endl;
  //
  // Parameter generation test
  //
  cout << ++testNum << ". Generating curve parameters";
  if (PRE1_generate_params(gParams) == FALSE) {
    cout << " ... FAILED" << endl;
  } else {
    cout << " ... OK" << endl;
    testsSuccess++;
  }

  //
  // Key generation tests
  //
  cout << ++testNum << ". Generating keypair 1";
  ProxyPK_PRE1 pk1;
  ProxySK_PRE1 sk1;
  if (PRE1_keygen(gParams, pk1, sk1) == FALSE) {
    cout << " ... FAILED" << endl;
  } else {
    cout << " ... OK" << endl;
    testsSuccess++;
  }

  cout << ++testNum << ". Generating keypair 2";
  ProxyPK_PRE1 pk2;
  ProxySK_PRE1 sk2;
  if (PRE1_keygen(gParams, pk2, sk2) == FALSE) {
    cout << " ... FAILED" << endl;
  } else {
    cout << " ... OK" << endl;
    testsSuccess++;
  }

  //
  // Re-encryption key generation test
  //
  cout << ++testNum << ". Re-encryption key generation test ";
  ECn delKey;
  // Generate a delegation key from user1->user2
  if (PRE1_delegate(gParams, pk2, sk1, delKey) == FALSE) {
    cout << " ... FAILED" << endl;
  } else {
    cout << " ... OK" << endl;
    testsSuccess++;
  }

  //
  // First-level encryption/decryption test
  //
  cout << ++testNum << ". First-level encryption/decryption test ";
  Big plaintext1 = 100;
  Big plaintext2 = 0;
  ProxyCiphertext_PRE1 ciphertext;
  if (PRE1_level1_encrypt(gParams, plaintext1, pk1, ciphertext) == FALSE) {
    cout << " ... FAILED" << endl;
  } else {
    // Decrypt the ciphertext
    if (PRE1_decrypt(gParams, ciphertext, sk1, plaintext2) == FALSE) {
      cout << " ... FAILED" << endl;
    } else {
      if (plaintext1 != plaintext2) {
	cout << " ... FAILED" << endl;
      } else {
	cout << " ... OK" << endl;
	testsSuccess++;
      }
    }
  }

  //
  // Second-level encryption/decryption test
  //
  cout << ++testNum << ". Second-level encryption/decryption test ";
  plaintext1 = 100;
  plaintext2 = 0;
  if (PRE1_level2_encrypt(gParams, plaintext1, pk1, ciphertext) == FALSE) {
    cout << " ... FAILED" << endl;
  } else {
    // Decrypt the ciphertext
    if (PRE1_decrypt(gParams, ciphertext, sk1, plaintext2) == FALSE) {
      cout << " ... FAILED" << endl;
    } else {
      if (plaintext1 != plaintext2) {
	cout << " ... FAILED" << endl;
      } else {
	cout << " ... OK" << endl;
	testsSuccess++;
      }
    }
  }

  //
  // Re-encryption/decryption test
  //
  ProxyCiphertext_PRE1 newCiphertext;
  plaintext2 = 0;
  cout << ++testNum << ". Re-encryption/decryption test ";
  // Re-encrypt ciphertext from user1->user2 using delKey
  // We make use of the ciphertext generated in the previous test.
  if (PRE1_reencrypt(gParams, ciphertext, delKey, newCiphertext) == FALSE) {
    cout << " ... FAILED" << endl;
  } else {
    // Decrypt the ciphertext
    if (PRE1_decrypt(gParams, newCiphertext, sk2, plaintext2) == FALSE) {
      cout << " ... FAILED" << endl;
    } else {
      if (plaintext1 != plaintext2) {
	cout << " ... FAILED" << endl;
      } else {
	cout << " ... OK" << endl;
	testsSuccess++;
      }
    }
  }

  // 
  // Proxy non-invisibility (negative) test
  //
  // We take the re-encrypted ciphertext from the previous test
  // and relabel it as a first-level ciphertext.  In PRE1 the
  // first-level and re-encrypted ciphertexts have different
  // forms, and hence the ciphertext should decrypt incorrectly.
  //
  cout << ++testNum << ". Proxy non-invisibility test ";
  newCiphertext.type = CIPH_FIRST_LEVEL;
  // Decrypt the ciphertext
  if (PRE1_decrypt(gParams, newCiphertext, sk2, plaintext2) == FALSE) {
    cout << " ... FAILED" << endl;
  } else {
    if (plaintext1 == plaintext2) {
      cout << " ... FAILED" << endl;
    } else {
      cout << " ... OK" << endl;
      testsSuccess++;
    }
  }

  //
  // Serialization/Deserialization test
  //
  BOOL serTestResult = TRUE;
  cout << ++testNum << ". Serialization/deserialization tests";
  char buffer[1000];
  
  // Serialize a public key
  int serialSize = pk1.serialize(SERIALIZE_BINARY, buffer, 1000);
  ProxyPK_PRE1 newpk;
  newpk.deserialize(SERIALIZE_BINARY, buffer, serialSize);
  serTestResult = serTestResult && (newpk == pk1);

  // Serialize a secret key
  serialSize = sk1.serialize(SERIALIZE_BINARY, buffer, 1000);
  ProxySK_PRE1 newsk;
  newsk.deserialize(SERIALIZE_BINARY, buffer, serialSize);
  serTestResult = serTestResult && (newsk == sk1);

  // Serialize a ciphertext
  serialSize = newCiphertext.serialize(SERIALIZE_BINARY, buffer, 1000);
  ProxyCiphertext_PRE1 newerCiphertext;
  newerCiphertext.deserialize(SERIALIZE_BINARY, buffer, serialSize);
  serTestResult = serTestResult && (newerCiphertext == newCiphertext);

  // Serialize curve parameters
  serialSize = gParams.getSerializedSize(SERIALIZE_BINARY);
  serialSize = gParams.serialize(SERIALIZE_BINARY, buffer, 1000);
  CurveParams newParams;
  newParams.deserialize(SERIALIZE_BINARY, buffer, serialSize);
  serTestResult = serTestResult && (newParams == gParams);

  if (serTestResult == TRUE) {
    cout << " ... OK" << endl;
    testsSuccess++;
  } else {
    cout << " ... FAILED" << endl;
  }
  
  // ******
  // PRE2 Tests
  // ******

  cout << endl << "TESTING PRE2 ROUTINES" << endl << endl;
  //
  // Parameter generation test
  //
  cout << ++testNum << ". Generating curve parameters";
  if (PRE2_generate_params(gParams) == FALSE) {
    cout << " ... FAILED" << endl;
  } else {
    cout << " ... OK" << endl;
    testsSuccess++;
  }

  //
  // Key generation tests
  //
  cout << ++testNum << ". Generating keypair 1";
  ProxyPK_PRE2 ppk1;
  ProxySK_PRE2 ssk1;
  if (PRE2_keygen(gParams, ppk1, ssk1) == FALSE) {
    cout << " ... FAILED" << endl;
  } else {
    cout << " ... OK" << endl;
    testsSuccess++;
  }

  cout << ++testNum << ". Generating keypair 2";
  ProxyPK_PRE2 ppk2;
  ProxySK_PRE2 ssk2;
  if (PRE2_keygen(gParams, ppk2, ssk2) == FALSE) {
    cout << " ... FAILED" << endl;
  } else {
    cout << " ... OK" << endl;
    testsSuccess++;
  }


  //
  // Re-encryption key generation test
  //
  cout << ++testNum << ". Re-encryption key generation test ";
  // Generate a delegation key from user1->user2
  if (PRE2_delegate(gParams, ppk2, ssk1, delKey) == FALSE) {
    cout << " ... FAILED" << endl;
  } else {
    cout << " ... OK" << endl;
    testsSuccess++;
  }

  //
  // First-level encryption/decryption test
  //
  cout << ++testNum << ". First-level encryption/decryption test ";
  plaintext1 = 100;
  plaintext2 = 0;
  ProxyCiphertext_PRE2 cciphertext;
  if (PRE2_level1_encrypt(gParams, plaintext1, ppk1, cciphertext) == FALSE) {
    cout << " ... FAILED" << endl;
  } else {
    // Decrypt the ciphertext
    if (PRE2_decrypt(gParams, cciphertext, ssk1, plaintext2) == FALSE) {
      cout << " ... FAILED" << endl;
    } else {
      if (plaintext1 != plaintext2) {
	cout << " ... FAILED" << endl;
      } else {
	cout << " ... OK" << endl;
	testsSuccess++;
      }
    }
  }

  //
  // Second-level encryption/decryption test
  //
  cout << ++testNum << ". Second-level encryption/decryption test ";
  plaintext1 = 100;
  plaintext2 = 0;
  if (PRE2_level2_encrypt(gParams, plaintext1, ppk1, cciphertext) == FALSE) {
    cout << " ... FAILED" << endl;
  } else {
    // Decrypt the ciphertext
    if (PRE2_decrypt(gParams, cciphertext, ssk1, plaintext2) == FALSE) {
      cout << " ... FAILED" << endl;
    } else {
      if (plaintext1 != plaintext2) {
	cout << " ... FAILED" << endl;
      } else {
	cout << " ... OK" << endl;
	testsSuccess++;
      }
    }
  }

  //
  // Re-encryption test
  //
  ProxyCiphertext_PRE2 nnewCiphertext;
  plaintext2 = 0;
  cout << ++testNum << ". Re-encryption/decryption test ";
  // Re-encrypt ciphertext from user1->user2 using delKey
  if (PRE2_reencrypt(gParams, cciphertext, delKey, nnewCiphertext) == FALSE) {
    cout << " ... FAILED" << endl;
  } else {
    // Decrypt the ciphertext
    if (PRE2_decrypt(gParams, nnewCiphertext, ssk2, plaintext2) == FALSE) {
      cout << " ... FAILED" << endl;
    } else {
      if (plaintext1 != plaintext2) {
	cout << " ... FAILED" << endl;
      } else {
	cout << " ... OK" << endl;
	testsSuccess++;
      }
    }
  }

  // 
  // Proxy invisibility test
  //
  // We take the re-encrypted ciphertext from the previous test
  // and mark it as a first-level ciphertext.  Decryption
  // should still work just fine.
  //
  cout << ++testNum << ". Proxy invisibility test ";
  nnewCiphertext.type = CIPH_FIRST_LEVEL;
  // Decrypt the ciphertext
  if (PRE2_decrypt(gParams, nnewCiphertext, ssk2, plaintext2) == FALSE) {
    cout << " ... FAILED" << endl;
  } else {
    if (plaintext1 != plaintext2) {
      cout << " ... FAILED" << endl;
    } else {
      cout << " ... OK" << endl;
      testsSuccess++;
    }
  }

  //
  // Serialization/Deserialization test
  //
  serTestResult = TRUE;
  cout << ++testNum << ". Serialization/deserialization tests";
  
  // Serialize a public key
  serialSize = ppk1.serialize(SERIALIZE_BINARY, buffer, 1000);
  ProxyPK_PRE2 nnewpk;
  nnewpk.deserialize(SERIALIZE_BINARY, buffer, serialSize);
  serTestResult = serTestResult && (nnewpk == ppk1);
  
  // Serialize a secret key
  serialSize = ssk1.serialize(SERIALIZE_BINARY, buffer, 1000);
  ProxySK_PRE2 nnewsk1;
  nnewsk1.deserialize(SERIALIZE_BINARY, buffer, serialSize);
  serTestResult = serTestResult && (nnewsk1 == ssk1);
  
  // Serialize a ciphertext
  serialSize = newCiphertext.serialize(SERIALIZE_BINARY, buffer, 1000);
  ProxyCiphertext_PRE2 nnewerCiphertext;
  nnewerCiphertext.deserialize(SERIALIZE_BINARY, buffer, serialSize);
  serTestResult = serTestResult && (newerCiphertext == newCiphertext);

  if (serTestResult == TRUE) {
    cout << " ... OK" << endl;
    testsSuccess++;
  } else {
    cout << " ... FAILED" << endl;
  }

  cout << endl << "All tests complete." << endl;
  cout << testsSuccess << " succeeded out of " <<
    testNum << " total." << endl;
}

*/