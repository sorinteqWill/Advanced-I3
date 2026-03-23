from flask import Flask, jsonify, request, send_file
import random

app = Flask(__name__)

# Simulated victim database
victims_db = {}
for i in range(1, 101):
    victims_db[i] = {
        "user_id": i,
        "username": f"Victim_{i}_Corp",
        "email": f"admin@victim{i}corp.com",
        "crypto_wallet": f"bc1q{random.randint(100000,999999)}...mock...wallet",
        "ransom_paid": random.choice([True, False])
    }

@app.after_request
def add_simulated_headers(response):
    # Simulate a Cloudflare WAF environment
    response.headers['Server'] = 'cloudflare'
    response.headers['CF-RAY'] = 'mock-ray-id-12345'
    return response

@app.route('/')
def index():
    return "<h1>Phantom Ransomware Leak Portal</h1><p>Access Restricted.</p>"

@app.route('/favicon.ico')
def favicon():
    # Serves the icon for the icon_hasher.py script
    return send_file('favicon.ico', mimetype='image/vnd.microsoft.icon')

# The Vulnerable BOLA Endpoint
@app.route('/api/v1/victims/<int:victim_id>', methods=['GET'])
def get_victim(victim_id):
    # Require SOME token, simulating they logged in as an undercover user
    auth_header = request.headers.get('Authorization')
    if not auth_header or 'Bearer' not in auth_header:
        return jsonify({"error": "Unauthorized. Bearer token required."}), 401
    
    # BOLA FLAW: It checks if a token exists, but doesn't check WHICH user it belongs to.
    victim = victims_db.get(victim_id)
    if victim:
        return jsonify(victim), 200
    else:
        return jsonify({"error": "Victim ID not found"}), 404

if __name__ == '__main__':
    print("--- STARTING TARGET SIMULATION: ransom-leak-portal.io ---")
    print("[*] Vulnerable API active on /api/v1/victims/<id>")
    # Bind to 0.0.0.0 so students on the LAN can reach it
    app.run(host='0.0.0.0', port=80)
    