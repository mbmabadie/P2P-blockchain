import json
import os
import random

def gen_transactions(num_transactions = 10):
    transactions = {}
    for i in range(0, num_transactions):
        cur_transactions = {}
        first_person_index = random.randint(0,100)
        second_person_index = random.randint(0,100)
        amount = random.randint(1,1000)
        while first_person_index == second_person_index:
            second_person_index = random.randint(0,100)
            
        cur_transactions['transaction '+ str(i)] = ("person {0} sends {1} coins to person {2}".format(first_person_index, amount, second_person_index))
    
    return transactions


# for item in gen_transactions():
#     print(item)
        
current_dir_path = os.path.dirname(os.path.realpath(__file__))

with open(current_dir_path + '/transactions.json', 'w') as outfile:
    json.dump(gen_transactions(), outfile)
        
    
    
