# OwnCrypto
Simple blockchain architecture and cryptocurrency based on it

This project provides an opportunity to create your own cryptocurrency based on a simple blockchain architecture and interact with it through a web application in Flask

## Start

You need to create files for each node on your network based on the Crypto.py file by changing in the app.run () method, replacing the values of the port parameter with unique values for each node, as shown in the example

```
app.run(host = '0.0.0.0', port = 5000)
```

Next, run all node scripts, now you can create GET and POST requests to node addresses

## Cryptocurrency methods

### connect_node()

Called via /connect_node POST request

Connects nodes to a request node

Accepts the addresses of all nodes exclude the request node in json format:
```
{
	"nodes":["http://127.0.0.1:5001",
		 "http://127.0.0.1:5002",
		 "http://127.0.0.1:5003"]
}
```
Returns a response containing the data of the connected nodes and the HTTP code

### get_chain()

Called via /get_chain GET request

Returns the response containing the chain for the request node and the HTTP code

### add_transaction()

Called via /add_transaction POST request

Adds a transaction with the specified parameters

Accepts transaction data in JSON format:
```
{
	"sender": "",
	"receiver": "",
	"amount":
}
```

Returns a response containing data about the index of the block that accepted the transaction and the HTTP code

### mine_block()

Called via /mine_block GET request

Performs work on mining a new block on the request тщву

Returns a response containing data about new block

### is_valid()

Called via /is_valid GET request

Checks the current state of the blockchain on the request node

Returns blockchain status and HTTP code

### replace_chain()

Called via /replace_chain GET request

Replaces the blockchain at the request node with the longest chain among all network nodes

Returns data about the blockchain of the request node and the HTTP code
