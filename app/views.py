from flask import Blueprint, render_template

app_main=Blueprint('main', __name__)

@app_main.route('/')
@app_main.route('/register')
@app_main.route('/recognition')
@app_main.route('/edit')
@app_main.route('/configuration')
def index():
	return render_template('index.html')



