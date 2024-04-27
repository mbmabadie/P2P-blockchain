from cheese import cheese
from cheese import RacletteCheese
from ecdsa import VerifyingKey, SigningKey, SECP256k1
import json



class cheesChain:
    def __init__(self):
        self.chain = []
        self.pend_trans = []
        #Hardcoded no need to check it's validity only a 0
        self.chain.append(RacletteCheese())

    ## Check the validation of chain
    def chain_valid(self):
        i = 0
        valid = True

        while i <= len(self.chain) - 1 and valid == True:
            valid = self.cheese_valid(self.chain[i])
            i += 1
            # print(valid)
        return valid

    ## Check the validation of cheese
    def cheese_valid(self, to_validate):

        if isinstance(to_validate, RacletteCheese):
            return True

        previous = self.chain[to_validate.index - 1 ]
        # Previous cheese details in the chain
        if isinstance(previous, RacletteCheese):
            prev_index = 0
            prev_smell = 0

        else:
            prev_index = previous.index
            prev_smell = previous.current_smell
        


        # New cheese details to compare index, smell
        if not isinstance(to_validate, cheese):
            print("Not a valid cheese")
            return False
        new_index = to_validate.index - 1
        new_smell_parent = to_validate.previous_smell
        new_smell = to_validate.current_smell
        
        if new_smell[0:5] != "00000":
            return False

        # if new_index != prev_index:          # index = previous index + 1
        #     print("index Error!",new_index,prev_index)
        #     return False
        if new_smell_parent != prev_smell: # previous hash = parent smell
            print("Smells Error!")
            return False
        return True

    ##  PUBLIC AND PRIVATE KEYS
    def key_generator(self):
        sign_key = SigningKey.generate(curve=SECP256k1) #the elliptic curve used by Bitcoin
        private_strKey = sign_key.to_string().hex()
        verifying_key = sign_key.get_verifying_key()
        public_strKey = verifying_key.to_string().hex()
        return private_strKey, public_strKey

    ## signature= enc(private, T)
    def signature(self, T, private_strKey):
        private = bytes.fromhex(private_strKey)
        sign_key = SigningKey.from_string(private, curve=SECP256k1)
        signature = sign_key.sign(T).hex()
        return signature

    ## msg = (T, signature)
    def transaction_verification(self, T, signature, public_strKey):
        public = bytes.fromhex(public_strKey)
        verifying_key = VerifyingKey.from_string(public, curve=SECP256k1)
        verified = verifying_key.verify(bytes.fromhex(signature), T)
        return verified


    ## ((SenderPub, amount, ReceiverPub,), signature)
    def gen_transactions(self, public, private, public2, amount):
        msg = public + str(amount) + public2
        signature = self.signature(msg.encode('utf-8'), private)
        cur_transactions = ("person {0} sends {1} coins to person {2} signature {3} ".format(public, amount, public2, signature))
        return cur_transactions

    #return the length of the current
    def len_of_chain(self):
        return len(self.chain)


    def add_cheese(self,cheese):
        if self.cheese_valid(cheese) is True:
            self.chain.append(cheese)
            #self.blockchain_save(self)
        # return True # added??
        return self


    def blockchain_save(self,cheesechain):
        json_file = 'blockchain.json'  ## blockchain data file
        with open(json_file, 'w', encoding='utf-8') as file:
            json.dump(cheesechain, file, ensure_ascii=False)

    def blockchain_load(self, json_file):
        with open(json_file) as file:
            cheesechain = json.load(file)
            return cheesechain


