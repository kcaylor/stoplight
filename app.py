import time
import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

# Set up the app
app = Flask(__name__, static_folder='./frontend/build/',    static_url_path='/')

CORS(app)

max_updates = 45*10  # 45 updates per minute, 10 minutes

# Store student status updates
status_updates = []

# Serve React app static files
@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/status', methods=['POST'])
def post_status():
    global status_updates
    status = request.json.get('status')
    timestamp = time.time()
    status_updates.append({'status': status, 'timestamp': timestamp})
    if len(status_updates) > max_updates:
        # If there are more than 450 status updates, remove the oldest ones
        status_updates = status_updates[-max_updates:]
        return jsonify({'message': 'Too many updates in past 10 minutes'})
    else:
        return jsonify({'message': 'Status update received'})


@app.route('/api/status_summary', methods=['GET'])
def get_status_summary():
    global status_updates
    cutoff_time = time.time() - 600  # 10 minutes ago
    recent_updates = [update for update in status_updates if update['timestamp'] >= cutoff_time]

    red_count = sum(1 for update in recent_updates if update['status'] == 'red')
    green_count = sum(1 for update in recent_updates if update['status'] == 'green')
    yellow_count = sum(1 for update in recent_updates if update['status'] == 'yellow')
    total_count = len(recent_updates)

    return jsonify({
        'red': red_count / total_count if total_count > 0 else 0,
        'green': green_count / total_count if total_count > 0 else 0,
        'yellow': yellow_count / total_count if total_count > 0 else 0,
        'total': total_count
    })


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
