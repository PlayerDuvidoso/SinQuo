from flask import Blueprint, request

loginbp = Blueprint('login', __name__)

@loginbp.route('/', methods=['GET', 'POST'])
def login():
    

    if request.method == 'GET':
        return 'Free Fire'

    elif request.method == 'POST':
        return 'Free Fire Max'
