from flask import flash

import smtp_helper as smtp
import api_helper as api
from datetime import datetime

def activateUser(token):
    email = smtp.confirmToken(token)
    if email and api.get_user_by_email(email): 
        if(api.activate_user(email)):
            flash("Account activated successfully, please login.", "success")
            return True

    flash("Error activating account.", "error")
    return False

def registerUser(newUser):

    # Verificar se o email já está registado
    if api.get_user_by_email(newUser['email']):
        flash("Another user is already registered with this email.", "error")
        return False
    else:
        # Registar o utilizador no ficheiro
        api.create_user(newUser)

        # Enviar email de confirmação
        smtp.sendConfMail(newUser['email'])
        flash("We sent you an email to activate your account.", "success")
        return True
    
def loginUser(email, password):
    user = api.get_user_by_email(email)
    
    if not user:
        flash("Email is not registered.", "error")
        return False
    
    if not user.get('is_active', False):
        flash("Account not activated. Please check your email before logging in.", "warning")
        return False
    
    if user['password'] == password:
        flash("Login successful.", "success")
        #update last login time
        api.patch_user_by_id(user['id'], {"last_login": datetime.now().isoformat()})
        return True
    else:
        flash("Incorrect password.", "error")
        return False