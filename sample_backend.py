from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
import random
import string
from model_mongodb import User


app = Flask(__name__)

#CORS stands for Cross Origin Requests.
CORS(app) #Here we'll allow requests coming from any domain. Not recommended for production environment.

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/users', methods=['GET', 'POST'])
def get_users():
    if request.method == 'GET':
        search_username = request.args.get('name')
        search_job = request.args.get('job')
        if search_username and search_job:
            result = User().find_by_name_and_job(search_username, search_job) 
        elif search_username:
            result = User().find_by_name(search_username)
        else:
            result = User().find_all()
        return {"users_list": result}
    elif request.method == 'POST':
        userToAdd = request.get_json() # no need to generate an id ourselves
        newUser = User(userToAdd)
        newUser.save() # pymongo gives the record an "_id" field automatically
        resp = jsonify(newUser), 201
        return resp

@app.route('/users/<id>', methods=['GET', 'DELETE'])
def get_user(id):
    if request.method == 'GET':
        user = User({"_id":id})
        if user.reload() :
            return user
        else :
            return jsonify({"error": "User not found"}), 404
    elif request.method == 'DELETE':
        user = User({"_id":id})
        resp = user.remove()
        if resp['n'] == 0:
            return {}, 404
        return {}, 204