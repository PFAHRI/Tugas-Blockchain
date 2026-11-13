"""
LEVEL 8 (DEMO) — Node Blockchain lewat HTTP dengan Flask
========================================================

File ini SUDAH LENGKAP (tidak ada TODO). Gunakan untuk praktik di kelas setelah
level08_jaringan.py lulus tes: menjalankan beberapa node di port berbeda,
seperti endpoint di artikel GeeksforGeeks tetapi dengan jaringan.

Cara pakai (buka 3 terminal):
    python level08_server.py 5001
    python level08_server.py 5002
    python level08_server.py 5003

Lalu dari terminal ke-4 (atau browser / Postman):
    curl -X POST localhost:5001/nodes -H "Content-Type: application/json" \
         -d '{"nodes": ["http://localhost:5002", "http://localhost:5003"]}'
    curl localhost:5002/mine_block          # node 5002 menambang 2 blok
    curl localhost:5002/mine_block
    curl localhost:5001/get_chain           # masih 1 blok
    curl localhost:5001/resolve             # ambil rantai terpanjang dari peer
    curl localhost:5001/get_chain           # sekarang 3 blok
    curl localhost:5001/valid

Butuh:  pip install flask requests
"""

import sys

import requests
from flask import Flask, jsonify, request

from level08_jaringan import Node

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
app = Flask(__name__)
node = Node(f"node-{PORT}", difficulty=4)
peer_urls = set()


@app.get("/mine_block")
def mine_block():
    block = node.tambang_blok([f"hadiah untuk {node.nama}"])
    return jsonify({"message": "A block is MINED", **block}), 200


@app.get("/get_chain")
def get_chain():
    return jsonify({"chain": node.chain, "length": len(node.chain)}), 200


@app.get("/valid")
def valid():
    ok = node.rantai_valid(node.chain)
    return jsonify({"message": "The Blockchain is valid." if ok else "The Blockchain is not valid."}), 200


@app.post("/nodes")
def register_nodes():
    data = request.get_json(silent=True) or {}
    for url in data.get("nodes", []):
        peer_urls.add(url.rstrip("/"))
    return jsonify({"message": "Peer ditambahkan", "peers": sorted(peer_urls)}), 201


@app.get("/resolve")
def resolve():
    terpanjang = None
    for url in peer_urls:
        try:
            resp = requests.get(f"{url}/get_chain", timeout=5).json()
        except requests.RequestException:
            continue
        chain = resp["chain"]
        if len(chain) > len(terpanjang or node.chain) and node.rantai_valid(chain):
            terpanjang = chain
    if terpanjang:
        node.chain = terpanjang
        return jsonify({"message": "Rantai diganti dengan yang terpanjang", "length": len(node.chain)}), 200
    return jsonify({"message": "Rantai kita sudah yang terpanjang", "length": len(node.chain)}), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=PORT)
