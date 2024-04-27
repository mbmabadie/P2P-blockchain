import os
import datetime
from cheeseChain import cheesChain
from cheese import RacletteCheese
from  cheese import cheese

import pickle


def main():

    test = cheesChain()



    test2 = cheese(test.len_of_chain(),0,"IDKN")

    test = test.add_cheese(test2)

    print("AYO",test.chain_valid())
    print(test.len_of_chain())
    # file = open("CheeseChain.txt", "wb")
    #
    # formated = pickle.dumps(test)
    #
    # file.write(formated)
    # We can load the cheese chain data from this.





if __name__== "__main__":
    main()

