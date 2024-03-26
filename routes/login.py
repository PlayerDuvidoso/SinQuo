from flask import Blueprint, request, render_template
import flask_login

loginbp = Blueprint('login', __name__)

@loginbp.route('/', methods=['GET', 'POST'])
def login():
    
    if request.method == 'GET':
        return render_template('signup.html')

    elif request.method == 'POST':
        return render_template('signup.html')
