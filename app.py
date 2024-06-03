from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Example dictionary mapping drivers to countries
driver_countries = {
    'Max Verstappen': 'Netherlands',
    'Charles Leclerc': 'Monaco',
    'Lando Norris': 'United Kingdom',
    'Carlos Sainz Jnr': 'Spain',
    'Sergio Perez': 'Mexico',
    'Oscar Piastri': 'Australia',
    'George Russell': 'United Kingdom',
    'Lewis Hamilton': 'United Kingdom',
    'Fernando Alonso': 'Spain',
    'Yuki Tsunoda': 'Japan',
    'Lance Stroll': 'Canada',
    'Oliver Bearman': 'United Kingdom',
    'Nico Hulkenberg': 'Germany',
    'Daniel Ricciardo': 'Australia',
    'Alexander Albon': 'Thailand',
    'Esteban Ocon': 'France',
    'Kevin Magnussen': 'Denmark',
    'Pierre Gasly': 'France',
    'Zhou Guanyu': 'China',
    'Valtteri Bottas': 'Finland',
    'Logan Sargeant': 'United States'
}

@app.route('/update-standings', methods=['GET'])
def update_standings():
    url = 'https://www.bbc.co.uk/sport/formula1/standings#Drivers'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'aria-label': "Formula 1 Drivers' Standings"})
    rows = table.find_all('tr')[1:]  # Skip the header row

    standings = []
    for row in rows:
        cols = [col.get_text(strip=True) for col in row.find_all('td')]
        
        # Extract and clean the values
        rank = cols[0].split()[0]  # Only take the first part (rank number)
        driver = cols[1].strip()
        team = cols[2].strip()
        wins = cols[3].split()[0]  # Only take the first part (wins number)
        points = cols[4].split()[0]  # Only take the first part (points number)

        # Clean up driver name and abbreviation
        driver_abbr = driver[-3:].strip()  # Extract the last 3 characters as the abbreviation
        driver_name = driver[:-3].strip()  # Extract the rest as the name
        full_driver_name = f"{driver_name} {driver_abbr}"  # Ensure there is a space between name and abbreviation

        # Get country and map to flag URL
        country = driver_countries.get(driver_name, 'Unknown')
        flag_url = f"https://flagcdn.com/16x12/{country.lower().replace(' ', '-')}.png"

        standings.append({
            'rank': rank,
            'driver': full_driver_name,
            'team': team,
            'wins': wins,
            'points': points,
            'flag_url': flag_url
        })

    return jsonify(standings)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
