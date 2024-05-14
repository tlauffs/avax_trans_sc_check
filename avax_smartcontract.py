from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
from tqdm import tqdm

def connect():
    avax_c_w3 = Web3(HTTPProvider('https://api.avax.network/ext/bc/C/rpc'))
    avax_c_w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    return avax_c_w3


def getTransactionInput(transaction): 
    transaction = avax_c_w3.eth.get_transaction(transaction)
    transaction_input_data = transaction['input']
    if b'SMOKLM' in transaction_input_data: 
        return True
    return False

def getTransactionsSC(contract_address, start_block, end_block, chunk_size=2048):
    transaction_counter = 0
    transaction_hashes = []
    try:
        with tqdm() as pbar:
            while start_block <= end_block:
                end_chunk_block = min(start_block + chunk_size-1, end_block)
                transactions = avax_c_w3.eth.get_logs({
                    "fromBlock": start_block,
                    "toBlock": end_chunk_block,
                    "address": contract_address
                })
                for transaction in transactions:
                    if getTransactionInput(transaction.transactionHash.hex()):
                        transaction_hashes.append(transaction.transactionHash.hex())
                        transaction_counter += 1
                start_block += chunk_size
                pbar.update(1)
    except Exception as e:
        print("Error:", e)
    return transaction_hashes, transaction_counter

avax_c_w3 = connect()
start_block = 44900000
end_block = avax_c_w3.eth.block_number
step = 2048
contract_address = "0x215B2ae1E51A43f360901425Edf0e4fDDb30CA80"

print(f'Getting transaction_hashes with SMOKLM in input: for contract {contract_address} : starting form block : {44900000} untit block {end_block}')
transaction_hashes, transaction_counter =  getTransactionsSC(contract_address, start_block, end_block)
print('transaction_hashes with SMOKLM in input: ', transaction_counter)
print('amount of transactions with SMOKLM in input:  ', transaction_hashes)