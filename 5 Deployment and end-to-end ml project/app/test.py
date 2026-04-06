from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.post('/home')
def index():
    return jsonify({'message': 'hello DEPI'})

@app.get('/')
def home():
    return render_template('test.html')

app.run()
