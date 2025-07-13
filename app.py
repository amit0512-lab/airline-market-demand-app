from flask import Flask, render_template, request
import requests
import pandas as pd

app = Flask(__name__)

API_KEY = 'ffc625a931e29ea0e2f4d2403c8fe88a'
API_URL = 'http://api.aviationstack.com/v1/flights'

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    # Get form inputs
    dep_iata = request.form.get('dep_iata')

    # Make API request
    params = {
        'access_key': API_KEY,
        'limit': 100,
        'dep_iata': dep_iata
    }
    response = requests.get(API_URL, params=params)
    data = response.json()

    # Process data
    flights = data.get('data', [])

    routes = []
    airlines = []

    for flight in flights:
        dep = flight['departure']['iata'] if flight['departure'] else 'N/A'
        arr = flight['arrival']['iata'] if flight['arrival'] else 'N/A'
        airline = flight['airline']['name'] if flight['airline'] else 'N/A'
        routes.append(f"{dep} -> {arr}")
        airlines.append(airline)

    df = pd.DataFrame({
        'Route': routes,
        'Airline': airlines
    })

    top_routes = df['Route'].value_counts().head(5).to_dict()
    top_airlines = df['Airline'].value_counts().head(5).to_dict()

    return render_template('results.html',
                           routes=top_routes,
                           airlines=top_airlines)

if __name__ == '__main__':
    app.run(debug=True)
