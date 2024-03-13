from flask import Flask, render_template
from routes.login import loginbp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

app.register_blueprint(loginbp, url_prefix = '/login')

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)