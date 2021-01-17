from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
import random
import string
app = Flask(__name__)
CORS(app)

def randomID():
	a = random.choice(string.ascii_letters).lower()
	b = random.choice(string.ascii_letters).lower()
	c = random.choice(string.ascii_letters).lower()
	x = str(random.randint(0, 9))
	y = str(random.randint(0, 9))
	z = str(random.randint(0, 9))
	return a + b + c + x + y + z

@app.route('/')
def hello_world():
	return 'Hello, world!'

@app.route('/users', methods=['GET', 'POST', 'DELETE'])
def get_users():
	if request.method == 'GET':
		search_username = request.args.get('name')
		search_job =request.args.get('job')
		if search_username and search_job :
			subdict = {'users_list' : []}
			for user in users['users_list']:
				if user['name'] == search_username and user['job'] == search_job:
					subdict['users_list'].append(user)
			return subdict
		elif search_username :
			subdict = {'users_list' : []}
			for user in users['users_list']:
				if user['name'] == search_username:
					subdict['users_list'].append(user)
			return subdict
		return users
	elif request.method == 'POST':
		userToAdd = request.get_json()
		userToAdd['id'] = randomID()
		users['users_list'].append(userToAdd)
		resp = jsonify(userToAdd)
		resp.status_code = 201
		return resp
	elif request.method == 'DELETE':
		search_id = request.args.get('id')
		resp = jsonify(success=False)
		if search_id :
			subdict = []
			for user in users['users_list']:
				if user['id'] != search_id:
					subdict.append(user)
				else:
					resp = jsonify(success=True)
			users['users_list'] = subdict
		return resp

@app.route('/users/<id>', methods=['GET', 'DELETE'])
def get_user(id):
	if request.method == 'GET':
		if id :
			for user in users['users_list']:
				if user['id'] == id:
					return user
			return ({})
		return users
	elif request.method == 'DELETE':
		resp = jsonify(success=False)
		if id :
			subdict = []
			for user in users['users_list']:
				if user['id'] != id:
					subdict.append(user)
				else:
					resp = jsonify(success=True)
					#resp.status_code = 200
			users['users_list'] = subdict
		return resp

users = { 
	'users_list' :
	[
		{ 
			'id' : 'xyz789',
			'name' : 'Charlie',
			'job': 'Janitor',
		},
		{
			'id' : 'abc123', 
			'name': 'Mac',
			'job': 'Bouncer',
		},
		{
			'id' : 'ppp222', 
			'name': 'Mac',
			'job': 'Professor',
		}, 
		{
			'id' : 'yat999', 
			'name': 'Dee',
			'job': 'Aspring actress',
		},
		{
			'id' : 'zap555', 
			'name': 'Dennis',
			'job': 'Bartender',
		}
	]
}