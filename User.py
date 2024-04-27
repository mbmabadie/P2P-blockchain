#USER RELATED CODE IN THIS FILE
from ecdsa import VerifyingKey, SigningKey, SECP256k1
import os


##  PUBLIC AND PRIVATE KEYS
def key_generator():
    sign_key = SigningKey.generate(curve=SECP256k1)  # the elliptic curve used by Bitcoin
    private_strKey = sign_key.to_string().hex()
    verifying_key = sign_key.get_verifying_key()
    public_strKey = verifying_key.to_string().hex()
    return private_strKey, public_strKey


## signature= enc(private, T)
def signature(T, private_strKey):
    private = bytes.fromhex(private_strKey)
    sign_key = SigningKey.from_string(private, curve=SECP256k1)
    signature = sign_key.sign(T).hex()
    return signature

def verify_locally():
    if os.stat("Keys/public.txt").st_size == 0 or os.stat("Keys/private.txt").st_size == 0:
        #If file is empty
        return False
    else:
        return True


def generate_locally():
    priv,pub =key_generator()

    file = open("Keys/private.txt","w")

    file.write(priv)

    file.close()

    file = open("Keys/public.txt", "w")

    file.write(pub)

    file.close()






