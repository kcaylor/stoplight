import time
import os
import logging
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import redis
import threading

# Set up the app and logging
app = Flask(__name__, static_folder='./frontend/build/',    static_url_path='/')
CORS(app)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Redis connection
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
redis_store = redis.StrictRedis.from_url(REDIS_URL, decode_responses=True)

# Function to remove outdated status updates
def clean_status_updates():
    # we are going to remove status updates that are older than 20 minutes
    twenty_minutes_ago = time.time() - (20 * 60)
    for status in ['red', 'yellow', 'green']:
        num_removed = redis_store.zremrangebyscore(f'status_updates:{status}', '-inf', twenty_minutes_ago)
        if num_removed > 0:
            # log the number of removed status updates to the server console
            logger.info(f"Removed {num_removed} outdated '{status}' status updates")

    # Schedule the function to run again after 60 seconds
    threading.Timer(60, clean_status_updates).start()

# Start the scheduled task
clean_status_updates()

# Serve React app static files
@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/status', methods=['POST'])
def post_status():
    # Get the status update from the request and assign a timestamp
    status = request.json.get('status')
    timestamp = time.time()
    
    # Store the status update in Redis with a timestamp using the ZADD command
    status_key = f'status_updates:{status}'
    redis_store.zadd(status_key, {timestamp: timestamp})

    return jsonify({'message': 'Status update received', 
                    status_key: {'timestamp': timestamp}})

@app.route('/api/status_summary', methods=['GET'])
def get_status_summary():
    # We are only looking for updates in the last 10 minutes    
    ten_minutes_ago = time.time() - 600
    
    # Count the status updates in Redis
    red_count = redis_store.zcount('status_updates:red', ten_minutes_ago, '+inf')
    yellow_count = redis_store.zcount('status_updates:yellow', ten_minutes_ago, '+inf')
    green_count = redis_store.zcount('status_updates:green', ten_minutes_ago, '+inf')
    total_count = red_count + yellow_count + green_count
    
    # return the counts as JSON    
    return jsonify({
        'red': red_count / total_count if total_count > 0 else 0,
        'green': green_count / total_count if total_count > 0 else 0,
        'yellow': yellow_count / total_count if total_count > 0 else 0,
        'total': total_count
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)