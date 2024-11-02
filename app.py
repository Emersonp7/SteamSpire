from flask import Flask, render_template, url_for, request, jsonify
import requests
class Game:
    def __init__(self, day) -> None:      
        self.day = 30 if day > 30 else day
        self.expanded = False
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
        self.gears -= self.militaryZones * 10 # Military Zones
        self.steam += self.industrialZones
        if self.commercialZones > 0:
            self.gears += 25 + ((25 * self.citizens) / 100)
        self.steam -= self.citizens // 10
       
    def addMilitaryZone(self) -> None:
        if (self.zones <= 0):
            return
        self.zones -= 1
        self.militaryZones += 1
        self.standing += 1
    
    def removeMilitrayZone(self) -> None:
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
        self.zone -= 1
        self.residentZones += 1
        self.citizens += 5
        
    def addCommercialZone(self) -> None:
        self.zone -= 1
        self.commercialZones += 1

    def addIndustrialZone(self) -> None:
        self.zone -= 1
        self.indesutrialZones += 1


    def expandZones(self) -> None:
        if self.expanded:
            return
        if self.zones == 0:
            self.zones += 16 # 25 - 9 zones leaves 16 zones untouched 
            self.expanded = True

    def buyZone(self) -> None:
        pass
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