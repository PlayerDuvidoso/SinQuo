from flask import Flask, render_template
from routes.login import loginbp
from routes.validation import validationbp
from databases import database
import flask_login
import os


#   -->App Config<--
app = Flask(__name__)
app.secret_key = os.getenv('private_key')

#   -->Login Manager<--
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def user_loader(email):
    if not database.email_exists(email):
        return
    
    user = database.get_user(email)
    return user


@app.route('/')
def index():

    print(flask_login.current_user)
    if flask_login.current_user.is_authenticated:
        print('Rola')
        return render_template('profile_details.html')

    return render_template('index.html')

app.register_blueprint(loginbp, url_prefix = '/login')
app.register_blueprint(validationbp, url_prefix= '/validate')

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)