from flask import Flask, request, jsonify
import ipfshttpclient
import psycopg2
from web3 import Web3

app = Flask(__name__)

# Connect to IPFS
ipfs = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="timelock_db",
    user="postgres",
    password="yourpassword",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Connect to Ethereum (Smart Contract)
w3 = Web3(Web3.HTTPProvider("https://sepolia.infura.io/v3/YOUR_INFURA_KEY"))
contract_address = "0xYourSmartContractAddress"
abi = [/* ABI JSON FROM COMPILATION */]
contract = w3.eth.contract(address=contract_address, abi=abi)

@app.route('/upload', methods=['POST'])
def upload_evidence():
    file = request.files['file']
    file.save(file.filename)
    
    # Upload to IPFS
    res = ipfs.add(file.filename)
    ipfs_hash = res['Hash']

    # Store metadata in PostgreSQL
    cursor.execute("INSERT INTO evidence (ipfs_cid) VALUES (%s) RETURNING id", (ipfs_hash,))
    evidence_id = cursor.fetchone()[0]
    conn.commit()

    return jsonify({"message": "File uploaded", "ipfs_hash": ipfs_hash, "evidence_id": evidence_id})

@app.route('/get_evidence/<int:evidence_id>', methods=['GET'])
def get_evidence(evidence_id):
    cursor.execute("SELECT ipfs_cid FROM evidence WHERE id = %s", (evidence_id,))
    data = cursor.fetchone()
    if data:
        return jsonify({"ipfs_hash": data[0]})
    return jsonify({"error": "Evidence not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
