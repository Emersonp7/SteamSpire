from flask import Flask, render_template, send_from_directory, url_for, request, jsonify
from flask_cors import CORS
import requests, random

class Game:
    def __init__(self, day) -> None:      
        self.day = 30 if day > 30 else day
        self.startDay = 0
        self.expanded = False
        self.citizens = 0
        self.standing = 0

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
        
    def endDay(self) -> None:
        self.startDay += 1
        if self.startDay == self.day:
            score = self.citizens + self.standing + self.gears + self.steam
            print(score)
            return
        
        self.gears -= self.militaryZones * 10 # Military Zones
        self.steam += self.industrialZones

        if self.commercialZones > 0:
            self.gears += 25 + ((25 * self.citizens) / 100)

        self.steam -= self.citizens // 10
        self.expandZones()
       
    def addMilitaryZone(self) -> None:
        if (self.zones <= 0):
            return
        self.zones -= 1
        self.militaryZones += 1
        self.standing += 1
    
    def removeMilitaryZone(self) -> None:
        if self.militaryZones <= 0:
            return

        if self.TakeOver():
            self.zones += 1
            self.militaryZones -= 1
            self.standing -= 1

    def TakeOver(self) -> bool:
        random = random.randint(1, 101)
        percent = 75 if percent > 75 else 30 + self.standing * .1
        if random < percent:
            return True
        return False    

    def addResidentialZone(self) -> None:
        if (self.zones <= 0):
            return
        self.zones -= 1
        self.residentZones += 1
        self.citizens += 5
        
    def addCommercialZone(self) -> None:
        if (self.zones <= 0):
            return
        self.zones -= 1
        self.commercialZones += 1

    def addIndustrialZone(self) -> None:
        if (self.zones <= 0):
            return
        self.zones -= 1
        self.industrialZones += 1

    def expandZones(self) -> None:
        if self.expanded:
            return
        if self.zones == 0:
            self.zones += 16 # 25 - 9 zones leaves 16 zones untouched 
            self.expanded = True

    def setStatus(self, ZoneStatus, ZoneType):
        if ZoneStatus == "free":
            match ZoneType:
                case "R":
                    self.addResidentialZone()
                case "C":
                    self.addCommercialZone()
                case "I":
                    self.addIndustrialZone()
                case "M":
                    self.addMilitaryZone()
            return "owned"
    
    def buyZone(self, Zone, ZoneType) -> None:
        if not Zone:
            return
        
        zoneName = Zone["name"]
        zoneStatus = Zone["value"]
        
        if zoneStatus == "owned":
            return
        if self.gears < 100:

            if int(zoneName[1]) % 2 == 0 and self.citizens > 5:
                self.gears -= 50
                Zone["value"] = self.setStatus(zoneStatus, ZoneType)
                print(Zone, ZoneType)
                return

        if zoneName == "Z5" and zoneStatus == "free":
            Zone["value"] = self.setStatus(zoneStatus, ZoneType)
            print(Zone, ZoneType)
            return
        
        
        if int(zoneName[1]) % 2 != 0 and self.citizens > 10:
            self.gears -= 100
            Zone["value"] = self.setStatus(zoneStatus, ZoneType)
            print(Zone, ZoneType)
            return

app = Flask(__name__, template_folder='templates')
CORS(app)

global juego
juego = None

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/game', methods=['GET'])
def game():
    global juego
    days = int(request.args.get('days', 30))
    juego = Game(days)
    player_data = {
        'gears': juego.gears,
        'steam': juego.steam,
        'standing': juego.standing,
        'citizens': juego.citizens,
        'day': juego.startDay
    }
    return render_template('game.html', **player_data)

@app.route('/receive-cell-data', methods=['POST'])
def receive_cell_data():
    global juego
    if juego is None:
        return jsonify({"status": "error", "message": "Game instance not initialized"}), 400
    data = request.get_json()  # Get the JSON data sent by fetch
    print("Received cell data:", data)  # Print or process the received data
    ZoneType = data["selectedOption"]
    juego.buyZone(data, ZoneType)
    return jsonify(data)
    # return jsonify({"status": "success", "received_data": data})


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