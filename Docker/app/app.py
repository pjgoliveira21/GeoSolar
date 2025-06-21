import re
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
import logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['DEBUG'] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config[ 'SECRET_KEY' ] = '\xd0\xac\xb8\xac\xf4t\xd8\x0e=\xc2\xb6?@\xa2\xd4:wiVG\xd4\x97U\xde'

Session(app)

import auth_helper as auth_helper
import smtp_helper as smtp_helper
import api_helper as api

# Definição das expressões regulares
regex_patterns = {
    "email": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", #Formato padrão de email teste@teste.com
    "pwd": r"^[a-zA-Z0-9]{6,}$" 
}

@app.route('/')
def index():
    # check databases online
    print(api.get_station_service_health())
    if(not api.get_station_service_health()): flash("Stations Database is not available", "error")
    if(not api.get_user_service_health()): flash("Users Database is not available", "error")
     
    return redirect('/home')

@app.route('/home')
def home_page():
    return render_template('home.html',status="ok", apims="2", stationsms="4", usersms="4")

@app.route('/map/')
def map_page():
    return render_template('map.html', tL = request.args.get('targetLatitude', None), tLg = request.args.get('targetLongitude', None))

@app.route('/table')
def table():
    stations = api.get_stations(offset=0, limit=50)
    return render_template('table.html', stations=stations)

@app.route('/login')
def loginForm():
    # Se o utilizador já estiver logado, redireciona para a página inicial
    if(session.get('email')): 
        flash("Logout first", "warning")
        return redirect('/home')
    return render_template('login.html') 

@app.route('/actionLogin', methods=(['POST']))
def login():
    # Recebe os dados do formulário
    email = request.form['email']
    password = request.form['password']

    # Verifica se os dados inseridos estão corretos
    emailTest = re.search(regex_patterns['email'], email)
    
    if not emailTest: flash("Invalid email format.", "error")

    else:
        if(auth_helper.loginUser(email, password)):
            # Se o login for bem-sucedido, armazena o email na sessão
            session['email'] = email
            session['username'] = api.get_user_by_email(email).get('username', 'User')
            return redirect('/home')

    return redirect('/login')

@app.route('/register')
def registerForm():

    # Se o utilizador já estiver logado, redireciona para a página inicial
    if(session.get('email')): 
        flash("Logout first", "warning")
        return redirect('/home')
    
    return render_template("register.html")

@app.route('/actionRegister', methods=(['POST']))
def register():

    # Recebe os dados do formulário
    email = request.form['email']
    password = request.form['password']
    confirmPassword = request.form['confirmPassword']
    username = request.form['username']

    # Verifica se as passwords coincidem
    if password != confirmPassword:
        flash("Passwords do not match.", "error")
        return redirect('/register')

    # Verifica se os dados inseridos estão corretos
    emailTest = re.search(regex_patterns['email'], email)
    pwdTest = re.search(regex_patterns['pwd'], password)
    if not emailTest: flash("Invalid email format.", "error")
    if not pwdTest: flash("Invalid password format", "error")

    else:
        if(auth_helper.registerUser(newUser={'username': username, 'email': email, 'password': password})): return redirect('/home')

    return redirect('/register')

@app.route('/logout')
def logout():
    # Remove o email da sessão
    session.pop('email', None)
    session.pop('username', None)
    flash("Logout successful.", "success")
    return redirect('/home')
@app.route('/activate/<token>')
def confirm_email(token): 
    auth_helper.activateUser(token)
    return redirect('/home')

@app.route('/dashboard/sensors')
def sensor_dashboard():
    return render_template('dashboard_sensors.html')

@app.route('/getStations')
def get_stations_route():
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 0))
    search = request.args.get("search", "")
    stations = api.get_stations(offset=offset, limit=limit, search=search)
    return jsonify(stations)

@app.route('/getIotData')
def get_iot_data_route():
    return api.fetch_IOT()