from flask import Blueprint, request, render_template
import jwt
from databases import database

validationbp = Blueprint('validation', __name__)

def check_email(user_email: str):

    if user_email.find('@') < 0: #checks if the email has a handle
        status = 'Invalid email address'
        return {'status': f'{status}', 'isValid': False}
    
    elif len(user_email) > 50: #checks if the email is too long
        status = 'Email address too long'
        return {'status': f'{status}', 'isValid': False}

    elif not user_email.replace('.', '').split('@')[0].isalnum(): #checks if the email contains illegal characters (excludes the '.')
        status = 'Invalid email address'
        return {'status': f'{status}', 'isValid': False}

    return {'status': '', 'isValid': True}

def check_password(user_password: str):

    if len(user_password) < 6: #checks if the password is too short
        status = 'Password must be atleast 6 characters long'
        return {'status': f'{status}', 'isValid': False}
    
    return {'status': '', 'isValid': True}


@validationbp.route('/email', methods=['POST'])
def validate_email():

    user_email=request.form['useremail']
    email_check = check_email(user_email)
    
    return render_template('form_email.html', status=email_check['status'], useremail=user_email)

@validationbp.route('/password', methods=['POST'])
def validate_password():

    user_password=request.form['userpassword']
    password_check = check_password(user_password)
    
    return render_template('form_password.html', status=password_check['status'], userpassword=user_password)
    

@validationbp.route('/submit', methods=['POST'])
def validate_submit():

    user_email=request.form['useremail']
    user_password=request.form['userpassword']

    if check_email(user_email)['isValid'] and check_password(user_password)['isValid']:

        user_password = jwt.encode({'password': f'{user_password}'}, database.private_key, algorithm='HS256')

        if database.create_user(user_email, user_password, '', ''):

            return render_template('profile_details.html')

    
