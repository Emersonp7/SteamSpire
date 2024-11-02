from flask import Flask, render_template, url_for, request, jsonify
import requests

class Game:
    def __init__(self, day) -> None:
        self.day = day
        self.expand = False
        self.citizens = 0
        self.standing = 0 # One standing gives 10 percent

        # Map Zones
        self.zones = 9
        self.residentZones = 0
        self.commercialZones = 0
        self.industrialZones = 0
        self.militaryZones = 0

        # currency
        self.gears = 100
        # resources
        self.steam = 1 # One steam for 10 citizens
        
    def endDay(self):
        self.day -= 1
        self.gears -= self.militaryZones * 10
        if (self.citizens % 10 == 0):
            self.steam -= 1
        self.gears += 25 + ((25 * self.citizens)/100)

        
    def addMilitaryZone(self) -> None:
        if (self.zones <= 0):
            return
        self.zones -= 1
        self.militaryZones += 1


        

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/game')
def game():
    return render_template("game.html")

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