import random
import hashlib
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import re

public_keys = []
private_keys = []
for i in range(1000):
    new_key = RSA.generate(1024)
    public_key = new_key.exportKey("PEM")
    private_key = new_key.publickey().exportKey("PEM")
    with open("public234.txt", "a") as myfile:
        public_keys.append(public_key)
        string1 = str(public_key)

        string1 = string1.replace("b\'-----BEGIN RSA PRIVATE KEY-----", ' ')
        string1 = string1.replace("-----END RSA PRIVATE KEY-----\'", " ")

        myfile.write(string1)
        myfile.write('\n')

    with open("private234.txt", "a") as myfile:
        private_keys.append(private_key)
        string2 = str(private_key)

        string2 = string2.replace("b\'-----BEGIN PUBLIC KEY-----", ' ')
        string2 = string2.replace("-----END PUBLIC KEY-----\'", " ")

        myfile.write(string2)
        myfile.write('\n')

for i in range(50):
    x = random.randint(0, 999)
    y = random.randint(0, 999)
    while y == x:
        y = random.randint(0, 999)
    public_key_sender = public_keys[x]
    private_key_sender = private_keys[x]
    public_key_receiver = public_keys[y]
    private_key_receiver = private_keys[y]

    coins = random.randint(1, 10)
    Message = "Person " + str(x) + " sends " + str(coins) + " coins to person " + str(y)
    # print("Original message: ", Message)

    '''This steps is for encryption decryption'''
    Hash_M = hashlib.sha1(Message.encode()).hexdigest()
    # print("Hashing original message: ", Hash_M)
    message = str.encode(str(Hash_M) + " " + Message)
    # print("Hashing with message: ", message)

    RSA_private_Key = RSA.importKey(private_key_sender)
    OAEP_cipher = PKCS1_OAEP.new(RSA_private_Key)
    encryptedMsg = OAEP_cipher.encrypt(message)
    # print("Encryption of the sent message and signature", encryptedMsg)

    RSA_public_Key = RSA.importKey(public_key_sender)
    OAEP_cipher = PKCS1_OAEP.new(RSA_public_Key)
    decryptedMsg = OAEP_cipher.decrypt(encryptedMsg)
    # print('The original message sent after decryption :', decryptedMsg)

    '''These steps are to add more security and check if the hash received is the same as the hash that will be generated by receiver'''
    Hash_M_received = str(decryptedMsg).split(' ')[0]
    M_prime = str(decryptedMsg).split(' ')[1:]
    M_prime[-1] = str(M_prime[-1]).split('\'')[0]  # we remove ' in order to not affect the hash
    M_prime2 = ' '.join(M_prime)
    # print("Transaction info", M_prime2)  # this shows the sender, amount and receiver

    Hash_M_received = str(Hash_M_received).split('\'')[1]
    # print(Hash_M_received)  # just to get the output hash of the sender
    Hash_M2 = hashlib.sha1(M_prime2.encode()).hexdigest()
    Hash_M = hashlib.sha1(Message.encode()).hexdigest()
    Hash_M2 = str.encode(Hash_M2)
    M_prime2 = str.encode(M_prime2)
    RSA_private_Key = RSA.importKey(private_key_receiver)
    OAEP_cipher = PKCS1_OAEP.new(RSA_private_Key)
    encryptedMsg = OAEP_cipher.encrypt(Hash_M2)
    # print("Encryption of the received message and signature", encryptedMsg)

    RSA_public_Key = RSA.importKey(public_key_receiver)
    OAEP_cipher = PKCS1_OAEP.new(RSA_public_Key)
    decryptedMsg = OAEP_cipher.decrypt(encryptedMsg)
    # print('The original message sent after decryption :', decryptedMsg)

    # print(Hash_M_received)
    # print(decryptedMsg)
    decryptedMsg = str(decryptedMsg).split('\'')[1]
    # print(M_prime2)
    if decryptedMsg == Hash_M_received:
        # print("Done!")
        with open("list_of_transactions.txt", "a") as myfile:
            string3 = str(M_prime2)
            string3 = string3.split('\'')[1]
            # print(pers1)
            # print(pers2)
            # print(string3)
            pers1 = string3.split(" ")[1]
            # print(pers1)
            pers2 = string3.split(" ")[-1]
            # print(pers2)

            pers1 = int(re.findall("\d+", pers1)[0])
            pers2 = int(re.findall("\d+", pers2)[0])
            # print(pers1)
            # print(pers2)

            with open("public234.txt") as f:
                publicKey1 = f.readlines()[pers1].rstrip()
                # print(publicKey1)
            publicKey1 = publicKey1.split('\\n')[1]
            with open("public234.txt") as f:
                publicKey2 = f.readlines()[pers2].rstrip()
                # print(publicKey2)
            publicKey2 = publicKey2.split('\\n')[1]
            string3 = string3.replace("Person " + str(pers1), publicKey1)
            string3 = string3.replace("person " + str(pers2), publicKey2)
            # print(string3)

            # string3 = string3.replace()

            myfile.write(string3)
            myfile.write('\n')
