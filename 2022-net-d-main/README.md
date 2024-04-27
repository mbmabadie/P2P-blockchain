# 2022-net-d


## Introduction
We implemented a Peer-to-Peer network which emulates the mining process of a blockchain. A peer will try to join the network and find a valid cheese and add it to the cheese chain which they will propagate around the rest of the network. 

## Instructions 
You need pip and some libraries to use our project. Run these two commands to install the libraries: 
- pip install ecdsa
- pip install Crypto


To start the network, one must run tracker.py first. This will initialize a server to store all the peers' IPs and ports. Then, on the same network, one must run peer.py and enter the IP and port provided by the tracker. At this point, the peer will start mining and information about the blockchain (i.e. number of peers, blockchain size) will be displayed in the terminal. More peers can join from either the same terminal or from other computers on the same network. 

<h2>Architecture</h2>
<h3>Cheese/cheese chain</h3>
The cheese code describes how the blocks are created. The cheese chain describes the entire process of the blockchain, including adding and validating cheese. 

<h3>Tracker</h3>
The tracker maintains a list of all connected users' IPs and ports. When a user connects to the tracker, it adds the new users' IP and port and provides its contents to the new user.

<h3>Peer</h3>
A peer tries to join the network by asking the tracker for all connected users and tries to connect to them by their IPs and ports. <br />
It will create two threads. One will receive data and one will send data. An empty cheese chain is initialized when the program starts. <br />
If the peer receives a cheese chain that is valid and longer in the listening thread, then it will adopt it as its new cheese chain. Otherwise, it will ignore it. <br />
In the sending thread, the peer constantly searches for new cheese. When it finds one, the peer adds the cheese to its cheese chain and sends the cheese chain to other peers. 
