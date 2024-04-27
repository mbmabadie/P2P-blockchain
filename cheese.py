import hashlib
import random
import re


class cheese:
    
    def __init__(self, index, previous_smell, data):
        # data has to at most 60 bit (60 characters)
        # blanks = " "
        # self.data =    + (60 - len(data)) * blanks
        self.data = data
        self.previous_smell = previous_smell
        self.index = index
        to_be_hashed = str(self.index) + str(self.data) + str(previous_smell)
        
        check = None

        while check is None:
            self.nonce = str(random.randint(10000000, 99999999))
            temp_smell = hashlib.sha1((to_be_hashed+self.nonce).encode()).hexdigest()

            #print(temp_smell)

            check = re.search('^00000', temp_smell)

        #print(21*'-' + "first cheese created" + 21*'-')
        self.current_smell = temp_smell
        
    def get_cheese(self):
            # bits represents characters in a string becasue we are sending cheese(block) as a sequence of characters 
            content = ""
            content += self.index # 8bits => content[0:8]
            content += self.previous_smell # 40 bits => content[8:48]
            content += self.current_smell # 40 bits => content[48:88]
            content += self.data # 38 bits => content[88:]
            
            return content # 126 bits

class RacletteCheese:
    def __init__(self):
        self.data = 0
        self.index = 0
        self.current_smell = 0


