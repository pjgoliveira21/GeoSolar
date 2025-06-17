from flask import Flask, render_template, request
import os
from api_helper import get_stations
from dotenv import load_dotenv
import logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/map/')
def map_page():
    return render_template('map/map.html')

@app.route('/table')
def table():
    stations = get_stations(offset=0, limit=50)
    return render_template('table.html', stations=stations)

@app.route('/login')
def login():
    return render_template('login.html') 

@app.route('/register')
def register():
    return render_template('register.html') 

@app.route('/dashboard/sensors')
def sensor_dashboard():
    return render_template('dashboard_sensors.html')

@app.route('/getStations')
def get_stations_route():
    offset = int(request.args.get('offset', 0))
    limit = int(request.args.get('limit', 0))
    return get_stations(offset=offset, limit=limit)
