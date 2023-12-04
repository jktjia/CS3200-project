from flask import Blueprint, request, jsonify, make_response
import json
from src import db


user = Blueprint('user', __name__)

# get saved logs
@user.route('/user/<id>/saves', methods=['GET'])
def get_saved(id):
    cursor = db.get_db().cursor()
    cursor.execute(f'select log_id from user_saved_logs\
        inner join users on users.id = user_saved_logs.user_id\
        inner join logs on logs.id = user_saved_logs.log_id\
            where user_id = {id}')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# get follows
@user.route('/user/<id>/follow/user', methods=['GET'])
def get_saved(id):
    cursor = db.get_db().cursor()
    cursor.execute(f'''select user_id from user_follows_users where 
    follower_id = {id}
    ''')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get customer detail for customer with particular userID
@user.route('/user/<userID>', methods=['GET'])
def get_customer(userID):
    cursor = db.get_db().cursor()
    cursor.execute('select * from user where id = {0}'.format(userID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response