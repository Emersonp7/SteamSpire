import React, { Component } from 'react';
import './App.css';
import Card from './Card';

class App extends Component {
  constructor(props) {
    super(props);
    const urlParams = new URLSearchParams(window.location.search);
    const days = urlParams.get('days') ? parseInt(urlParams.get('days'), 10) : 7; // Default to 7 if not set

    this.state = {
      gears: 100,
      steam: 1,
      standing: 0,
      citizens: 0,
      zonesOwned: 0,
      dayCounter: 1,
      selectedZones: Array(9).fill(null), // Array to store selected zones
      zoneOptions: [
        { title: "Industrial Zone", description: "Increases steam production" },
        { title: "Residential Zone", description: "Increases population" },
        { title: "Commercial Zone", description: "Generates gears" },
      ],
      totalDays: days,
    };
  }

  // Calculate cost based on plot index, making plot 5 (index 4) free
  calculateCost = (plotIndex) => {
    if (plotIndex === 4) {
      return { gears: 0, citizensRequired: 0 }; // Free plot
    }
    const isOdd = (plotIndex + 1) % 2 !== 0;
    return {
      gears: isOdd ? 100 : 50,
      citizensRequired: isOdd ? 10 : 5
    };
  }

  // Handle plot click for choosing a zone
  handlePlotClick = (plotIndex) => {
    const { gears, citizens, selectedZones, zoneOptions } = this.state;
    
    // Check if the plot already has a zone assigned
    if (selectedZones[plotIndex] !== null) {
      alert("This plot already has a zone and cannot be changed.");
      return;
    }

    const cost = this.calculateCost(plotIndex);

    // For plot 5, skip the resource check
    if (plotIndex !== 4 && (gears < cost.gears || citizens < cost.citizensRequired)) {
      alert("Not enough resources to select this zone.");
      return;
    }

    const zoneChoice = prompt(
      "Choose a zone:\n1: Industrial\n2: Residential\n3: Commercial"
    );

    if (zoneChoice >= 1 && zoneChoice <= 4) {
      const selectedZone = zoneOptions[zoneChoice - 1];

      this.setState((prevState) => {
        let updatedCitizens = prevState.citizens;
        
        // Increase citizens by 5 if "Residential Zone" is selected
        if (selectedZone.title === "Residential Zone") {
          updatedCitizens += 5;
        }

        return {
          gears: plotIndex === 4 ? prevState.gears : prevState.gears - cost.gears, // Deduct only gears
          zonesOwned: prevState.zonesOwned + 1,
          citizens: updatedCitizens,
          selectedZones: prevState.selectedZones.map((zone, index) =>
            index === plotIndex ? selectedZone : zone
          )
        };
      });
    } else {
      alert("Invalid choice.");
    }
  }

  // Calculate daily resource changes
  incrementDay = () => {
    if (this.state.dayCounter === this.state.totalDays) {
      // End game when day limit is reached
      this.calculateFinalScore();
      return;
    }

    let industrialZones = 0;
    let commercialZones = 0;

    // Count each type of zone
    this.state.selectedZones.forEach(zone => {
      if (zone) {
        if (zone.title === "Industrial Zone") industrialZones += 1;
        if (zone.title === "Commercial Zone") commercialZones += 1;
      }
    });

    // Calculate new resource values
    const newSteam = this.state.steam + industrialZones;
    const baseGearsGain = 25 * commercialZones;
    const citizenBonusGears = Math.floor((25 * this.state.citizens) / 100);
    const newGears = this.state.gears + baseGearsGain + citizenBonusGears;

    // Update state with new resources and increment day
    this.setState((prevState) => ({
      steam: newSteam,
      gears: newGears,
      dayCounter: prevState.dayCounter + 1,
    }));
  }

  // Calculate final score based on formula and display it as a pop-up
  calculateFinalScore = () => {
    const { gears, citizens, zonesOwned, steam } = this.state;
    const score = (gears + citizens) * (zonesOwned + steam);
    alert(`Game Over! Your final score is: ${score}. Thanks for playing!`);
  }

  render() {
    return (
      <div>
        <div className='playerinfo'>
          <p>Gears: {this.state.gears}</p>
          <p>Steam: {this.state.steam}</p>
          <p>Citizens: {this.state.citizens}</p>
          <p>Military Standing: {this.state.standing}</p>
          <p>Zones Owned: {this.state.zonesOwned}</p>
          <p>Day {this.state.dayCounter}/{this.state.totalDays}</p>
        </div>

        <div className="grid-container">
          {this.state.selectedZones.map((zone, index) => (
            <div
              key={index}
              className="grid-item"
              onClick={() => this.handlePlotClick(index)}
            >
              {zone ? (
                <Card title={zone.title} description={zone.description} />
              ) : (
                <div>
                  <p>Plot {index + 1}</p>
                  {index === 4 ? (
                    <p>Free Spot</p>
                  ) : (
                    <p>Cost: {this.calculateCost(index).gears} Gears, requires {this.calculateCost(index).citizensRequired} Citizens</p>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>

        <div className="button">
          <button onClick={this.incrementDay}>End Day</button>
        </div>
      </div>
    );
  }
}

export default App;