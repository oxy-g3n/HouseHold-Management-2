from flask import Flask, render_template
from project_APIs import create_app
from flask_cors import CORS
from itsdangerous import URLSafeTimedSerializer
app = Flask(__name__)
SECRET_KEY = 'A_KEY'
app.secret_key = SECRET_KEY
app.config['SECRET_KEY'] = SECRET_KEY
CORS(app, resources={r"/*": {"origins": "*"}})
s = URLSafeTimedSerializer(SECRET_KEY)

@app.route('/')
@app.route('/home')
def index():
	return "Hello World!"


app = create_app()
if __name__ == '__main__':
	app.run(debug=False)
