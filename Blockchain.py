import hashlib
import json
import os
from collections import Counter
from datetime import datetime
from typing import Optional, Dict, List

from flask import (
    Flask, abort, jsonify, make_response, redirect,
    render_template, request, session, url_for, flash
)
from web3 import Web3
from web3.exceptions import ContractLogicError
from dotenv import load_dotenv
from functools import wraps

# Load environment variables
load_dotenv()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = os.getenv('FLASK_SECRET_KEY', os.urandom(24))
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True

# Blockchain configuration
RPC_URL = os.getenv('BLOCKCHAIN_RPC_URL')
CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS')
CONTRACT_ABI = json.loads(os.getenv('CONTRACT_ABI'))

# Initialize Web3
web3 = Web3(Web3.HTTPProvider(RPC_URL))
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

# Candidate mapping
CANDIDATES = {
    'a': 'Cristiano Ronaldo',
    'b': 'Neymar',
    'c': 'Lionel Messi'
}

class VoteIDGenerator:
    
    @staticmethod
    def generate_vote_id(aadhar_number: str, timestamp: str) -> str:
        """Generate a unique vote ID using Aadhar number and timestamp"""
        data = f"{aadhar_number}-{timestamp}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    @staticmethod
    def verify_vote_id(vote_id: str) -> bool:
        """Verify if a vote ID is valid"""
        return bool(vote_id and len(vote_id) == 64 and all(c in '0123456789abcdef' for c in vote_id))

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to check if user is an admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            flash('Admin access required.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        aadhar_number = request.form.get('aadhar_number')
        name = request.form.get('name')
        
        if not aadhar_number or not name:
            flash('Please fill in all fields.', 'error')
            return render_template('login.html')
        
        # Generate vote ID
        vote_id = VoteIDGenerator.generate_vote_id(
            aadhar_number,
            datetime.now().isoformat()
        )
        
        session['user_id'] = vote_id
        session['name'] = name
        
        return redirect(url_for('vote'))
    
    return render_template('login.html')

@app.route('/vote', methods=['GET', 'POST'])
@login_required
def vote():
    if request.method == 'POST':
        choice = request.form.get('candidate')
        
        if not choice or choice not in CANDIDATES:
            flash('Invalid candidate selection.', 'error')
            return render_template('vote.html', candidates=CANDIDATES)
        
        try:
            # Submit vote to blockchain
            tx_hash = contract.functions.vote(CANDIDATES[choice]).transact({
                'from': web3.eth.accounts[0]
            })
            
            # Wait for transaction confirmation
            web3.eth.wait_for_transaction_receipt(tx_hash)
            
            flash('Vote submitted successfully!', 'success')
            return redirect(url_for('thank_you'))
            
        except ContractLogicError as e:
            flash(f'Error submitting vote: {str(e)}', 'error')
            return render_template('vote.html', candidates=CANDIDATES)
    
    return render_template('vote.html', candidates=CANDIDATES)

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # In production, use proper authentication
        if username == os.getenv('ADMIN_USERNAME') and \
           password == os.getenv('ADMIN_PASSWORD'):
            session['is_admin'] = True
            return redirect(url_for('results'))
        
        flash('Invalid credentials.', 'error')
    
    return render_template('admin_login.html')

@app.route('/results')
@admin_required
def results():
    try:
        # Get results from blockchain
        results = {
            candidate: contract.functions.getVoteCount(idx).call()
            for idx, candidate in enumerate(CANDIDATES.values())
        }
        
        total_votes = sum(results.values())
        
        return render_template(
            'results.html',
            results=results,
            total_votes=total_votes
        )
        
    except Exception as e:
        flash(f'Error fetching results: {str(e)}', 'error')
        return redirect(url_for('admin_login'))

@app.route('/verify', methods=['GET', 'POST'])
def verify_vote():
    if request.method == 'POST':
        vote_id = request.form.get('vote_id')
        
        if not VoteIDGenerator.verify_vote_id(vote_id):
            flash('Invalid vote ID format.', 'error')
            return render_template('verify.html')
        
        try:
            # In production, implement secure vote verification
            vote_info = contract.functions.getVoteInfo(vote_id).call()
            return render_template('verify.html', vote_info=vote_info)
            
        except Exception as e:
            flash('Vote not found or error occurred.', 'error')
    
    return render_template('verify.html')

@app.route('/thank-you')
@login_required
def thank_you():
    return render_template('thank_you.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Check if required environment variables are set
    required_env_vars = [
        'FLASK_SECRET_KEY',
        'BLOCKCHAIN_RPC_URL',
        'CONTRACT_ADDRESS',
        'CONTRACT_ABI',
        'ADMIN_USERNAME',
        'ADMIN_PASSWORD'
    ]
    
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    if missing_vars:
        raise RuntimeError(
            f"Missing required environment variables: {', '.join(missing_vars)}"
        )
    
    # Check blockchain connection
    if not web3.is_connected():
        raise RuntimeError("Cannot connect to blockchain network")
    
    app.run(debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true')