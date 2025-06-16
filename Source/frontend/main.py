import os
from flask import Flask, flash, redirect, send_file, render_template, request, session, jsonify,url_for
from flask_session import Session

from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer

import logging,json,requests,re
from datetime import datetime

API_URL="http://127.0.0.1:5000"
USERS_FILE = "private/users.json"
STATION_PHOTO_FOLDER = "./static/images/stations"


# Inicialização do Flask
app = Flask(__name__)
app.url_map.strict_slashes = False
app.config[ 'TEMPLATES_AUTO_RELOAD' ] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config[ 'UPLOAD_FOLDER' ] = STATION_PHOTO_FOLDER
logging.basicConfig( level=logging.DEBUG )
Session(app)

# Inicialização do Mail
app.config[ 'MAIL_SERVER' ]= 'smtp.gmail.com'
app.config[ 'MAIL_PORT' ] = 465
app.config[ 'MAIL_USERNAME' ] = 'pjg.oliveira21@gmail.com'
app.config[ 'MAIL_PASSWORD' ] = 'miiljqvzmrpthiac'
app.config[ 'MAIL_USE_TLS' ] = False
app.config[ 'MAIL_USE_SSL' ] = True
app.config[ 'SECRET_KEY' ] = '\xd0\xac\xb8\xac\xf4t\xd8\x0e=\xc2\xb6?@\xa2\xd4:wiVG\xd4\x97U\xde'
mail = Mail(app)
s = URLSafeTimedSerializer(app.secret_key)

# Gerar token para confirmação de email
def genToken(email): return s.dumps(email, salt='email-confirm')

# Confirmar token de email
def confirmToken(token, expiration=3600):
    try: email = s.loads(token, salt='email-confirm', max_age=expiration)
    except Exception: return False
    return email

def activateUser(email):
    users = readJSON(USERS_FILE)
    if email in users:
        # Ativar a conta do utilizador apenas se já não estiver ativada
        if users[email]['activated']: return False
        
        users[email]['activated'] = True
        writeJSON(USERS_FILE,users)
        return True
    return False

# Enviar email de confirmação
def sendConfMail(dest, mail):
    token = genToken(dest)
    confirm_url = url_for('confirm_email', token=token, _external=True)
    _subject = 'Activate your GeoSolar account'
    _senderName = 'GeoSolar Team'
    _senderEmail = 'pjg.oliveira21@gmail.com'
    _msgContent = render_template('verifyEmailTemplate.html', verification_link=confirm_url)
    
    msg = Message(
        subject=_subject,
        sender=(_senderName, _senderEmail),
        recipients=[dest]
    )
    msg.html = _msgContent
    mail.send(msg)

# Definição das expressões regulares
regex_patterns = {
    "email": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", #Formato padrão de email teste@teste.com
    "pwd": r"^(?=.*\d)[a-zA-Z\d]{4,8}$" # 4 a 8 caracteres e pelo menos 1 número
}

# Função para ler ficheiros JSO
def readJSON(file):
    with open(file, 'r') as f: data = json.load(f)
    return data

# Função para escrever num ficheiro JSON
def writeJSON(file, data):
    with open(file, 'w') as f: json.dump(data, f, indent=4)

# Função para chamar a API externa com umza query específica
def callAPI(query):
    try:
        url=API_URL+query
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        logging.error(f"Error fetching data: {e}")

    return data

# Rotas base
# Rota para a página inicial
@app.route('/')
def getRoot(): return render_template("/pages/indexTemplate.html")

# Rota para aceder às expressões regulares
@app.route('/get-regex')
def get_regex(): return jsonify(regex_patterns)

# Rota para aceder ao favicon
@app.route('/favicon.ico')
def getFavicon(): return send_file( "./static/favicon.ico", as_attachment=True, max_age=1 )

# Rotas autenticação
# Rota para aceder ao formulário de registo
@app.route('/createaccount')
def registerForm():

    # Se o utilizador já estiver logado, redireciona para a página inicial
    if(session.get('email')): 
        flash("Logout first", "warning")
        return redirect('/')
    
    return render_template("/pages/registerFormTemplate.html")

# Rota para fazer login
@app.route('/login', methods=(['POST']) )
def login():
    # Recebe os dados do formulário
    email = request.form['email']
    pwd = request.form['pwd']
    users=readJSON(USERS_FILE)

    # Verificar correspondência entre email e password
    if email in users and users[email]['password'] == pwd:
        session['email'] = email
        session['activated'] = users[email]['activated']
        if not users[email]['activated']: flash("Remember to activate your account!", "warning")
        return redirect('/')
    else:
        flash("Email or password incorrect.", "error")  # Mensagem de erro
        return redirect('/')

# Rota para fazer um registo
@app.route('/register', methods=['POST'] )
def register():
    # Recebe os dados do formulário
    email = request.form['email']
    pwd = request.form['pwd']

    # Verifica se os dados inseridos estão corretos
    emailTest = re.search(regex_patterns['email'], email)
    pwdTest = re.search(regex_patterns['pwd'], pwd)
    if emailTest and pwdTest:

        users=readJSON(USERS_FILE)

        # Verificar se o email já está registado
        if email in users:
            flash("Another user is already registered with this email.", "error")
            return redirect('/createaccount')
        else:
            # Registar o utilizador no ficheiro
            users[email] = {'password': pwd}
            users[email]['activated'] = False
            users[email]['mystations'] = []
            writeJSON(USERS_FILE, users)

            # Enviar email de confirmação
            sendConfMail(email, mail)
            flash("We sent you an email to activate your account.", "success")
            return redirect('/')
    else:
        flash("An error ocurred.", "error")
        return redirect('/createaccount')

# Rota para fazer logout
@app.route('/logout')
def logout():

    # Se o utilizador não estiver logado, redireciona para a página inicial
    if(not session.get('email')): 
        flash("Not logged in", "warning")
        return redirect('/')

    # Terminar a sessão e redirecionar para a página inicial
    session['email'] = None
    session['activated'] = None
    flash("Logged out", "success")
    return redirect("/")

# Rota para ativar a conta
@app.route('/activate/<token>')
def confirm_email(token):
    email = confirmToken(token)
    if email and activateUser(email): flash("Account activated! Please Login.", "success")
    else: flash("Error activating account.", "error")
    return redirect('/')

# Rotas de páginas
# Rota para aceder à página de estações adicionadas pelo utilizador
@app.route('/mystations')
def mystations(): 
    # Se o utilizador não estiver logado ou tiver a conta por ativar, redireciona para a página inicial
    if(not session.get('email')): 
        flash("Not logged in", "warning")
        return redirect('/')
    
    if(not session.get('activated')): 
        flash("Activate your account to add and view added stations", "warning")
        return redirect('/')
    
    return render_template("/pages/myStationsTemplate.html")

@app.route('/addMyStation', methods=['POST'])
def addmystation():

    # Recebe os dados do formulário
    stationName = request.form['stationName']
    stationCapacity = request.form['stationCapacity']
    stationLatitude = request.form['stationLat']
    stationLongitude = request.form['stationLng']
    stationContinent = request.form['stationContinent']
    stationCountry = request.form['stationCountry']

    # Converter a string ISO para um objeto datetime
    dateObj = datetime.fromisoformat(datetime.now().isoformat())

    # Formatar para um formato legível (ex: "14 janeiro 2025, 15:30")
    timestamp = dateObj.strftime("%d %B %Y, %H:%M")

    users = readJSON(USERS_FILE)
    email = session.get('email')
    if email:
        # Se o utilizador escolheu imagem de satélite, apenas define a string "sat" no campo da imagem
        if request.form['imgSrc'] == 'sat': stationImg = "sat"

        # Caso contrário, obtem a imagem do formulario e guarda a imagem no diretório
        else: 
            stationImg = request.files['stationImg']
            stationImg.save( os.path.join( app.config['UPLOAD_FOLDER'], stationImg.filename))
        
        # Adiciona a nova estação ao ficheiro JSON
        new_station = {
            "name": stationName,
            "capacity": stationCapacity,
            "country": stationCountry,
            "continent": stationContinent,
            "latitude": stationLatitude,
            "longitude": stationLongitude,
            "img": stationImg.filename,
            "timestamp": timestamp
        }
        users[email]['mystations'].append(new_station)

        # Atualiza o ficheiro JSON
        writeJSON(USERS_FILE, users)
        flash("Station added successfully.", "success")
    else:
        flash("User not logged in.", "error")

    return redirect('/')
    
# Rota para aceder à página de mapa
@app.route('/map', methods=['GET'])
def render_map():
    # Recebe as opções possíveis para os filtros e envia para a página
    options = callAPI('/get-possible-values')
    return render_template("/pages/mapTemplate.html", options=options)

# Rota para pedir novas estações ao servidor
@app.route('/getStations', methods=['POST'])
def getStations():
    # Recebe a query enviada pelo JavaScript
    data = request.json
    query_string = data.get('filters')
    stations = callAPI(f'/get-station?{query_string}')

    importUserStations = data.get('showMyStations')
    myStationsOnly = data.get('myStationsOnly')

    # Se for usado o argumento de importar estações do utilizador, adiciona as estações do utilizador
    if (importUserStations):
        userEmail = session.get('email')
        userStations = readJSON(USERS_FILE)[userEmail]['mystations']

        # Se for usado o argumento de importar APENAS E SÓ as estações do utilizador, retorna APENAS E SÓ as estações do utilizador
        if(myStationsOnly): stations = userStations
        else: stations += userStations
        
    return stations