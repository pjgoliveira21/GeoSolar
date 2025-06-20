from flask import render_template, url_for
from app import app
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer

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

# Enviar email de confirmação
def sendConfMail(dest):
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