from flask import Flask, render_template, url_for

class Game:
    def __init__(self, day) -> None:
        self.day = day
        self.expand = False
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
        
    def endDay(self):
        self.day -= 1
        self.gears -= self.militaryZones * 10
        self.updateResources()
    
    def updateResources(self):
        return None


app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/game')
def game():
    return render_template("game.html")


if __name__ == "__main__":
    app.run(debug=True)