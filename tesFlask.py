from flask import Flask,request,jsonify
from flask_cors import CORS, cross_origin
from Baca_Mifare import ResultMifar1k
from CardMon import TapN


app=Flask(__name__)
CORS(app)

@app.route('/')
def teswa():
    return 'wadaaaa w'

@app.route('/checknfc_pr')
@cross_origin()
def Bacanfc():
    a=""
    if TapN()=="Tap":
       a=jsonify({'nis':ResultMifar1k()})
    else:
        a = jsonify({'nis': "Tap Kartu untuk Absen!"})
    return a

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

# @app.route('/shutdown')
# def shutdown():
#     shutdown_server()
#     return 'Server shutting down...'


app.run()