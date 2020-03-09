# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 18:44:35 2020

@author: Keith
"""

import datetime
import json

import requests
from flask import render_template, redirect, request

from app import app

# Node in the blockchain network that our application will communicate with
# to fetch and add data.
CONNECTED_NODE_ADDRESS = "http://127.0.0.1:8000"

posts = []

def fetch_posts():
    """
    Function to fetch the chain from a blockchain node, parse the
    data, and store it locally.
    """
    get_chain_address = "{}/chain".format(CONNECTED_NODE_ADDRESS)
    response = requests.get(get_chain_address)
    if response.status_code == 200:
        content = []
        chain = json.loads(response.content)
        for block in chain["chain"]:
            for tx in block["transactions"]:
                tx["index"] = block["index"]
                tx["hash"] = block["previous_hash"]
                content.append(tx)

        global posts
        posts = sorted(content,
                       key=lambda k: k['timestamp'],
                       reverse=True)
        
@app.route('/submit', methods=['POST'])
def submit_textarea():
    """
    Endpoint to create a new transaction via our application
    """
    post_content = request.form["content"]
    author = request.form["author"]

    post_object = {
        'author': author,
        'content': post_content,
    }

    # Submit a transaction
    new_tx_address = "{}/new_transaction".format(CONNECTED_NODE_ADDRESS)

    requests.post(new_tx_address,
                  json=post_object,
                  headers={'Content-type': 'application/json'})

    # Return to the homepage
    return redirect('/')