import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
import Blockchain
from uuid import uuid4
from urllib.parse import urlparse

node_address = str(uuid4()).replace('-', '')

app = Flask(__name__)

blockchain = Blockchain.Blockchain()

@app.route('/mine_block', methods = ['GET'])
def mine_block():
        previous_block = blockchain.get_previous_block()
        previous_proof = previous_block['proof']
        proof = blockchain.proof_of_work(previous_proof)
        previous_hash = blockchain.hash_(previous_block)
        blockchain.add_transaction(sender = node_address, receiver = '', amount = 1)
        block = blockchain.create_block(proof, previous_hash)
        responce = {'message': 'Block is mined',
                    'index': block['index'],
                    'timestamp': block['timestamp'],
                    'proof': block['proof'],
                    'previous_hash': block['previous_hash'],
                    'transactions': block['transactions']}
        return jsonify(responce), 200

@app.route('/get_chain', methods = ['GET'])
def get_chain():
        responce = {'chain': blockchain.chain,
                    'length': len(blockchain.chain)}
        return jsonify(responce), 200
    
@app.route('/is_valid', methods =['GET'])
def is_valid():
        is_valid = blockchain.is_chain_valid(blockchain.chain)
        if is_valid:
            responce = {'message': 'Blockchain is valid'}
        else:
            responce = {'message': 'Blockchain is not valid'}
        return jsonify(responce), 200
    
@app.route('/add_transaction', methods =['POST'])
def add_transaction():
    json = request.get_json()
    transaction_key = ['sender', 'receiver', 'amount']
    if not all (key in json for key in transaction_key):
        return 'Some elements of the transaction are missing', 400
    index = blockchain.add_transaction(json['sender'], json['receiver'], json['amount'])
    responce = {'message': f'This transation will be added to Block {index}'}
    return jsonify(responce), 201

@app.route('/connect_node', methods =['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return 'No node', 400
    for node in nodes:
        blockchain.add_node(node)
    responce = {'message': 'All the nodes are now connected. The Blockchain now contains the following nodes:',
                'total_nodes': list(blockchain.nodes)}
    return jsonify(responce), 201

@app.route('/replace_chain', methods =['GET'])
def replace_chain():
        is_chain_replaced = blockchain.replace_chain()
        if is_chain_replaced:
            responce = {'message': 'The nodes had different chains so the chain was replaced by the longest chain',
                        'new_chain': blockchain.chain}
        else:
            responce = {'message': 'The chain is the largest one',
                        'actual_chain': blockchain.chain}     
        return jsonify(responce), 200

app.run(host = '0.0.0.0', port = 5000)