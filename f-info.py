from flask import Flask, render_template
import base64
import requests
import json

app = Flask(__name__)

@app.route('/')
def index():
    username = 'your_username'
    password = 'your_password'
    url = 'https://opensky-network.org/api/states/all'
    username_bytes = username.encode('utf-8')
    password_bytes = password.encode('utf-8')
    credentials = base64.b64encode(username_bytes + b':' + password_bytes)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic ' + credentials.decode('utf-8')
    }
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    if 'states' in data:
        flights = []
        for flight in data['states']:
            callsign = flight[1]
            longitude = flight[5]
            latitude = flight[6]
            altitude = flight[7]
            speed = flight[9]
            track = flight[10]
            flights.append({
                'callsign': callsign,
                'longitude': longitude,
                'latitude': latitude,
                'altitude': altitude,
                'speed': speed,
                'track': track
            })
        return render_template('flight_data.html', flights=flights)
    else:
        return 'No flight data available.'

if __name__ == '__main__':
    app.run(debug=True)
