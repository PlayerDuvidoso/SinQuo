from flask import Blueprint, request, render_template

validationbp = Blueprint('validation', __name__)

@validationbp.route('/email', methods=['POST'])
def validate_email():

    user_email=request.form['useremail']

    if user_email.find('@') < 0:
        status = f'Invalid Email'
        return render_template('form_email.html', status=status)
    
    return render_template('form_email.html', status='', useremail=user_email)

    
