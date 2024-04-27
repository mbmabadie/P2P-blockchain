import socket
import threading
from threading import Thread
import time
import random
import os
from cheeseChain import cheesChain
from cheese import cheese
import pickle


peer_index = None
Transactions = []
mycheesechain = cheesChain()


peer_socket_tracker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def get_open_port():
        import socket
        s_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_obj.bind(("",0))
        s_obj.listen(1)
        port = s_obj.getsockname()[1]
        s_obj.close()
        return port
    
PORT = get_open_port()
Listen_PORT = get_open_port()

IPv4_ADDRESS = socket.gethostbyname(socket.gethostname())

peer_socket_tracker.bind((IPv4_ADDRESS, PORT))

peers_to_be_connected = []
#Use this to send to other peers
connected_peers = [] # use this list to send new found blocks to other peers



def thread_receive_from_tracker():
    global message
    global peer_index
    while True:
        message = peer_socket_tracker.recv(1024).decode()
        #IF THE MESSAGE STARTS WITH ZERO THEN THE TRACKER ASKS THE PEER TO PROVIDE AN OPEN PORT
        if message[0] == '0':
            print("<" *39 +" Received from tracker "+ "<" *39)
            print("need {0} open_ports: \n".format(message[1:]))
            num_of_needed_open_ports = int(message[1:])
            thread_send_to_tracker(num_of_needed_open_ports)
            
        elif message[0] == '1':
            print("<" *39 +" Received from tracker "+ "<" *39)
            print("your peer ID: {0}".format(message[-1]))
            peers_details_list = message[1:-1].split('-')
            print("peer(s) to be connected:\n")
            
            for peer in peers_details_list:
                print(peer)
            
            ip_port_list = message[1:-1].split('-')
            for ip_port in ip_port_list[:-1]: 
                new_peer_IPv4, new_peer_port = ip_port.split(',')
                peers_to_be_connected.append((new_peer_IPv4, new_peer_port))

        
def connect_with_tracker():
    tracker_ip = input("Please enter the IP Address of tracker:\n")
    tracker_port = int(float(input("Please enter the PORT of tracker:\n")))
    peer_socket_tracker.connect((tracker_ip, tracker_port))
    print("\n" + "=" * 38+" successfully conncected "+ "=" *38 + "\n")
    
    thread_receive = threading.Thread(target=thread_receive_from_tracker)
    thread_receive.start()

def thread_send_to_tracker(num_of_needed_open_ports): 
    print(">" *41 + " sending to tracker "+ ">" *41)
    print(">granted open port: " + str(Listen_PORT) + "\n")
    peer_socket_tracker.send(str(Listen_PORT).encode())



peer_socket_listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect_to_other_peers():
    print("=" * 38 + " connecting active peers " + "=" * 38)
    print('number of peers to be connected:' +  str(len(peers_to_be_connected)) + "\n")

    if len(peers_to_be_connected) > 0:
        connect_request()
        time.sleep(1)
        print("=" * 32+" successfully conncected to all peers "+ "=" *32 + "\n")

        peer_socket_listen.bind((IPv4_ADDRESS, Listen_PORT))
        thread_accept = threading.Thread(target=accept_peers) 
        thread_accept.start()
    else:

        peer_socket_listen.bind((IPv4_ADDRESS, Listen_PORT))
        thread_accept = threading.Thread(target=accept_peers) 
        thread_accept.start()
        
def connect_request():
    for peer in peers_to_be_connected:
        peer_socket_connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("trying to connect ({0}, {1}) ".format(peer[0],peer[1]))
        peer_socket_connect.connect((peer[0], int(peer[1])))
        print("successfully connceted to ({0}, {1}) \n".format(peer[0],peer[1]))
        start_receiving_blocks_thread(peer_socket_connect)
        connected_peers.append(peer_socket_connect)
        
    for i in range(len(peers_to_be_connected)):
        peers_to_be_connected.pop()


def accept_peers():
    global mycheesechain
    global connected_peers

    while True:
        peer_socket_listen.listen()
        peer_socket, peer_addr = peer_socket_listen.accept()
        connected_peers.append(peer_socket)
        start_receiving_blocks_thread(peer_socket)
        print("successfully connceted to {0} \n".format(peer_addr))
        Formated_data = pickle.dumps(mycheesechain)
        for others in connected_peers:
            others.send(Formated_data)
        print("We sent to ", len(connected_peers), "peers","\n", flush=True)
        time.sleep(2)
        
def thread_receive_from_other_peers(sokcet_obj):
    global mycheesechain

    while True:
        try:
            Formated_Data = sokcet_obj.recv(5000000)
            new_chain = pickle.loads(Formated_Data)

            if isinstance(new_chain,cheesChain):
                print("<" * 40+" cheesechain received "+ "<" *40,flush=True)
                if new_chain.chain_valid() and new_chain.len_of_chain() > mycheesechain.len_of_chain():
                    print("updated my cheesechain\n", flush=True)
                    mycheesechain = new_chain
                    print("cheesechain size: ", mycheesechain.len_of_chain(), "\n")
                else:
                    print("The cheesechain that has been received is not valid and is ignored\n", flush=True)
            else:
                print("<" * 40+" cheesechain received "+ "<" *40,flush=True)
                print("@" * 8+" It is not a cheschain instance "+ "@" *8,flush=True)

        except:
            print("=x=" * 7 +" peer" + str(sokcet_obj.getpeername())+ " disconnected from the network " + "=x=" * 7 + "\n")
            sokcet_obj.close()
            break


def start_receiving_blocks_thread(socket_obj):
    peer_thread = threading.Thread(target=thread_receive_from_other_peers, args=(socket_obj,))
    peer_thread.start()

def saveCheeseChain():
    global mycheesechain
    Formated_Data = pickle.dumps(mycheesechain)
    file = open("CheeseChain.txt", "wb")
    file.write(Formated_Data)


def verifyCheesechain():
    if os.stat("CheeseChain.txt").st_size == 0:
        print("Ourselves : No cheese chain found localy. We work with an empty cheese chain ")


    else:
        file = open("CheeseChain.txt","rb")
        Formated_data = file.read()
        mycheesechain = pickle.loads(Formated_data)
        
def read_transactions_list():
    global Transactions
    with open("list_of_transactions.txt") as f:
        Transactions = f.readlines()
        
# def choose_a_transaction():
#     tran =  random.choice(Transactions)
#     Transactions.remove(tran)
#     return tran

# Thread to find cheese and send it to other peers
def FindingCheese():
    global mycheesechain
    global connected_peers
    def process():

        while True:

            print("=?=" * 12 +" trying to find a valid cheese "+ "=?=" *12 + "\n\n",flush=True)
            print(Transactions[mycheesechain.len_of_chain()])
            newcheese = cheese(mycheesechain.len_of_chain(), mycheesechain.chain[-1].current_smell, Transactions[mycheesechain.len_of_chain()])
            print("==^==" * 8 +" I have found a cheese "+ "==^==" * 8,flush=True)
            mycheesechain.add_cheese(newcheese)
            print("cheesechain size: ", mycheesechain.len_of_chain(), "\n")
            Formated_data = pickle.dumps(mycheesechain)
            print(">" * 41+" sending cheesechain "+ ">" *41 + "\n",flush=True)
            for others in connected_peers:

                try:
                    others.send(Formated_data)

                except:
                    others.close
                    connected_peers.remove(others)

            time.sleep(2)


    t = Thread(target=process)
    t.start()


# def handledisconnect:


def main():

    connect_with_tracker()
    time.sleep(2)
    
    connect_to_other_peers()
    
    read_transactions_list()

    # #if locally I have no cheesechain
    # verifyCheesechain()

    if isinstance(mycheesechain,cheesChain):
        pass
        # print("So far so good")
    else:
        print("Error : cheesechain not initalized")
        exit()


    #Thread to find some cheese
    FindingCheese()




if __name__== "__main__":
    main()