# Se importaron las librerias necesarias
import datetime
import hashlib
import json

from flask import Flask, jsonify


class FirstBlockChain:

    # Constructor
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash='0')

    # Funcion para aniadir bloques a la cadena
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'time-stamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous-hash': previous_hash}
        self.chain.append(block)
        return block

    # Devuelve el ultimo bloque de la cadena
    def print_previous_block(self):
        return self.chain[-1]

    # Funcion de prueba de trabajo
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False

        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        encode_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encode_block).hexdigest()

    def chain_validator(self, chain):
        previous_block = chain[0]
        block_index = 1

        while block_index < len(chain):
            block = chain[block_index]
            if block['previous-hash'] != self.hash(previous_block):
                return False
            previous_block = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof ** 2 - previous_block ** 2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True


# Creacion de la web app usando flask
app = Flask(__name__)

# Crear objeto blockchain
blockchain = FirstBlockChain()


# Minar nuevo bloque
@app.route('/mine-block', methods=['GET'])
def mine_block():
    previous_block = blockchain.print_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    actual_hash = blockchain.hash(block)
    response = {'message': 'New block mining',
                'index': block['index'],
                'time-stamp': block['time-stamp'],
                'proof': block['proof'],
                'previous-hash': block['previous-hash'],
                'hash': actual_hash}
    return jsonify(response), 200


# Funcion para obtener la cadena
@app.route('/get-chain', methods=['GET'])
def display_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200


# Validacion de la blockchain
@app.route('/valid', methods=['GET'])
def validate_blockchain():
    valid = blockchain.chain_validator(blockchain.chain)
    if valid:
        response = {'messege': 'La blockchain funciona'}
    else:
        response = {'messege': 'La blockchain no funciona'}
    return jsonify(response), 200


app.run(host='0.0.0.0', port=5000)
