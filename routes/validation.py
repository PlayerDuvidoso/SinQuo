from flask import Blueprint, request, render_template
import jwt
from databases import database
from pydantic import BaseModel

validationbp = Blueprint('validation', __name__)

#   -->Response Model<--
class Response(BaseModel):
    status: str = ''
    isValid: bool = False

#   -->Validations<--
def check_email(user_email: str):

    if user_email.find('@') < 0: #checks if the email has a handle
        status = 'Invalid email address'
        return Response(status=status).model_dump()
    
    elif len(user_email) > 50: #checks if the email is too long
        status = 'Email address too long'
        return Response(status=status).model_dump()

    elif not user_email.replace('.', '').split('@')[0].isalnum(): #checks if the email contains illegal characters (excludes the '.')
        status = 'Invalid email address'
        return Response(status=status).model_dump()
    
    elif database.email_exists(user_email):
        status = 'Email already in use'
        return Response(status=status).model_dump()

    return Response(isValid=True).model_dump()

def check_password(user_password: str):

    if len(user_password) < 6: #checks if the password is too short
        status = 'Password must be atleast 6 characters long'
        return Response(status=status).model_dump()
    
    return Response(isValid=True).model_dump()

def check_username(username: str):

    if len(username) < 4 or len(username) > 20:
        status = 'Username Must at least 4 characters long and less than 20 characters long'
        return Response(status=status).model_dump()
    
    if not username.isalnum():
        status = 'Username must include only letters and numbers'
        return Response(status=status).model_dump()
    
    if database.username_exists(username):
        status = 'Username already taken'
        return Response(status=status).model_dump()

    return Response(isValid=True).model_dump()

def check_quote(userquote: str):

    if len(userquote) < 3 or len(userquote) > 150:
        status = 'Your Quote must have between 3 and 150 characters'
        return Response(status=status).model_dump()
    
    if database.quote_exists(userquote):
        status = 'Someone has already registered this Quote'
        return Response(status=status).model_dump()
    
    return Response(isValid=True).model_dump()

#   -->Routes<--
@validationbp.route('/email', methods=['POST'])
def validate_email():

    user_email=request.form['useremail'].strip()
    email_check = check_email(user_email)
    
    return render_template('form_email.html', status=email_check['status'], useremail=user_email)

@validationbp.route('/password', methods=['POST'])
def validate_password():

    user_password=request.form['userpassword'].strip()
    password_check = check_password(user_password)
    
    return render_template('form_password.html', status=password_check['status'], userpassword=user_password)
    
@validationbp.route('/username', methods=['POST'])
def validate_username():

    username=request.form['username'].strip()
    username_check=check_username(username)
    return render_template('form_username.html', status=username_check['status'], username=username)

@validationbp.route('userquote', methods=['POST'])
def validate_quote():
    userquote=request.form['userquote'].strip()
    userquote_check = check_quote(userquote)
    return render_template('form_quote.html', status=userquote_check['status'], userquote=userquote)

@validationbp.route('/submit', methods=['POST'])
def validate_submit():

    user_email=request.form['useremail'].strip()
    user_password=request.form['userpassword'].strip()
    username=request.form['username'].strip()
    userquote=request.form['userquote'].strip()

    if check_email(user_email)['isValid'] and check_password(user_password)['isValid'] and check_username(username)['isValid'] and check_quote(userquote)['isValid']:

        user_password = jwt.encode({'password': f'{user_password}'}, database.private_key, algorithm='HS256')
        database.create_user(user_email, user_password, username, userquote)

        return render_template('profile_details.html')

    
