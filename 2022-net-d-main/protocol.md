# Protocol TCP

##Cheese/CheeseChain
A raclette cheese is :
- Data that is intialized with a zero
- Index which is zero 
- Current smell which is zero 
     
A cheese is composed of :
- Data : It contains transaction
- Previous smell : contains smell of parent
- Index : Which index of the chain we are in 
- nonce : A random number 
- Current smell : It contains a hash of data 

A cheesechain is a 
- chain : That contains a list of all the cheese.



Our tracker tasks are : 

- Listening to incoming peers, adding them to the list of connected user
- Sending a list of all connected to peers to peers that are connected to the tracker.
- Keeping the peers updated with who joins the network.

Our p2p protocol is simple : <br/>

We start by connecting to the tracker and ask the list of connected users. <br/>
From a list of a connected user, we create two streams of data : 
- the first stream receives cheesechain from connected users and checks the validity of the chain, if it is valid we adopt the chain as our new chain, if it is not valid we ignore the chain.
- the second stream of data searches for cheese, adds it to it cheesechain, and sends the cheesechain to all the connected user.

We also handle in the peer file sudden peer disconnects.
