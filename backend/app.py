from flask import Flask, render_template, send_from_directory, jsonify, request
from flask_cors import CORS
import os
import requests

app = Flask(__name__, template_folder='templates')
CORS(app)

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/game', method=['GET'])
def game():
    if request.is_json:
        data = request.get_json()  # Get the JSON data
        # Logic for starting the game goes here
        return jsonify({"message": "Game started!", "status": "success"})
    else:
        return jsonify({"message": "Request must be JSON", "status": "error"}), 400
    # return send_from_directory('frontend/build', 'index.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('frontend/build/static', path)

@app.route('/story', methods=['GET'])
def story():
    cloudflare_url = 'https://old-forest-7d72.go48.workers.dev/'
    response = requests.get(cloudflare_url)

    if response.status_code == 200:
        story_data = response.json()
        return jsonify(story_data)
    else:
        return jsonify({'error': 'Failed to fetch story from AI.'}), 500

if __name__ == "__main__":
    app.run(debug=True)