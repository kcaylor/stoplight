import time
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# Store student status updates
status_updates = []

@app.route('/api/status', methods=['POST'])
def post_status():
    status = request.json.get('status')
    timestamp = time.time()
    status_updates.append({'status': status, 'timestamp': timestamp})
    return jsonify({'message': 'Status update received'})


@app.route('/api/status_summary', methods=['GET'])
def get_status_summary():
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
    app.run(debug=True, host='localhost', port=5000)
