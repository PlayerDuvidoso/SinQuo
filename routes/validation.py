from flask import Blueprint, request, render_template

validationbp = Blueprint('validation', __name__)

@validationbp.route('/email', methods=['POST'])
def validate_email():

    user_email=request.form['useremail']

    if user_email.find('@') < 0:
        status = 'Invalid email address'
        return render_template('form_email.html', status=status, useremail=user_email)
    
    elif len(user_email) > 50:
        status = 'Email address too long'
        return render_template('form_email.html', status=status, useremail=user_email)

    elif not user_email.replace('.', '').split('@')[0].isalnum():
        status = 'Invalid email address'
        return render_template('form_email.html', status=status, useremail=user_email)
    
    
    return render_template('form_email.html', status='', useremail=user_email)

@validationbp.route('/password', methods=['POST'])
def validate_password():

    user_password=request.form['userpassword']

    if len(user_password) < 6:
        status = 'Password must be atleast 6 characters long'
        return render_template('form_password.html', status=status, userpassword=user_password)
    
    return render_template('form_password.html', status='', userpassword=user_password)

@validationbp.route('/submit', methods=['POST'])
def validate_submit():
    pass

    
