import socket
import threading
import time

def get_open_port():
        import socket
        s_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_obj.bind(("",0))
        s_obj.listen(1)
        port = s_obj.getsockname()[1]
        s_obj.close()
        return port
 
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

PORT = 1234 #get_open_port()
IPv4_ADDRESS = socket.gethostbyname(socket.gethostname())

peers_socket_obj_list = []
peers_connection = {}

my_socket.bind((IPv4_ADDRESS, PORT))

def run():
    print("=" * 43+ " Tracker is Running "+ "=" *43)
    print("tracker_IPv4: " + IPv4_ADDRESS)
    print("tracker_PORT: " + str(PORT) +'\n')
    
    while True:
        global peers_connection
        my_socket.listen()
        peer_socket_obj, peer_addresses = my_socket.accept()
        
        joined_peer_ip = peer_addresses[0] # type(str)
        joined_peer_port = peer_addresses[1] # type(int)

        peers_socket_obj_list.append(peer_socket_obj)
        
        start_listenning_thread(peer_socket_obj)
        
        print("=" * 38+" new peer joined the netwrok "+ "=" *38)
        print("new_peer_IPv4: " + joined_peer_ip)
        print("new_peer_PORT: " + str(joined_peer_port) +'\n')
        
        request_listen_port(peer_socket_obj)
        
        time.sleep(1)
        
        if len(peers_connection.keys()) > 1:
            broadcast_connection_info()

def start_listenning_thread(peer):
    global peers_connection
    peer_thread = threading.Thread(target=listen_thread, args=(peer,)) 
    peer_thread.start()
    
def listen_thread(peer_socket_obj):
    global peers_connection
    while True:
        try:
            peer_ip = (peer_socket_obj.getpeername())[0] # type(str)
            message = peer_socket_obj.recv(1024).decode()
            if message:
                print("<" * 36+" Received from peer {0} ".format(peer_ip)+ "<" *36)
                print("granted open port: " + str(message)  +'\n')
                peers_connection[peer_socket_obj] = [peer_ip, message]
        except:
            print("=x=" * 8 + " peer " + str(peer_socket_obj.getpeername()) + " disconnected from the network " + "=x=" * 8 + "\n")
            peer_socket_obj.close()
            break
            


def request_listen_port(peers_socket_obj):
    peers_socket_obj.send(("0"+"1").encode())
        
def broadcast_connection_info():
    global peers_connection
    peers_sockets = list(peers_connection.keys())
    final_connectoin = ""
    for i in range(0, len(peers_sockets) - 1):
        connection = ""  
        peer_ip = peers_connection[peers_sockets[i]][0]
        connection += peer_ip + ','
        connection += peers_connection[peers_sockets[i]][1]  
        final_connectoin += connection + "-"
    peers_sockets[-1].send(("1" + final_connectoin + str(len(peers_sockets) - 1)).encode())
    time.sleep(1)
run()