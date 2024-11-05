from flask import Flask, render_template, send_from_directory, url_for, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/game')
def game():
    return send_from_directory('../frontend/build', 'index.html')

# Serve Flask static files (for homepage)
@app.route('/flask-static/<path:path>')
def serve_flask_static(path):
    return send_from_directory('static', path)

# Serve static assets for React from frontend/build/static
@app.route('/static/js/<path:path>')
def serve_react_js(path):
    return send_from_directory('../frontend/build/static/js', path)

@app.route('/static/css/<path:path>')
def serve_react_css(path):
    return send_from_directory('../frontend/build/static/css', path)

@app.route('/static/media/<path:path>')
def serve_react_media(path):
    return send_from_directory('../frontend/build/static/media', path)

# Serve assets in public directory, such as images or other media
@app.route('/public/<path:filename>')
def serve_public_file(filename):
    return send_from_directory('../frontend/public', filename)

@app.route('/story', methods=['GET'])
def story():
    cloudflare_url = 'https://old-forest-7d72.go48.workers.dev/'
    response = requests.get(cloudflare_url)
    if response.status_code == 200:
        story_data = response.json()
        return jsonify(story_data)
    else:
        return jsonify({'error': 'Failed to fetch story from AI.'}), 500

@app.route('/<path:path>', methods=['GET'])
def catch_all(path):
    if os.path.exists(os.path.join('../frontend/build', path)):
        return send_from_directory('../frontend/build', path)
    return send_from_directory('../frontend/build', 'index.html')

if __name__ == "__main__":
    app.run(debug=True)