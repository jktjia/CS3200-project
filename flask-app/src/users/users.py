from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


users = Blueprint('users', __name__)

#create a user
@users.route('/users', methods=['POST'])
def create_user():
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)
    
    #extracting the variable
    username = the_data['username']
    email = the_data['email']
    password = the_data['password']
    birthday = the_data['birthday']
    first_name = the_data['first_name']
    last_name = the_data['last_name']

    # Constructing the query
    query = 'insert into users (username, email, password, birthday, first_name, last_name) values ("'
    query += username + '", "'
    query += email + '", "'
    query += str(password) + '", "'
    query += str(birthday) + '", "'
    query += first_name + '", "'
    query += last_name + '")'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

#edit a user
@users.route('/users/<id>', methods=['PUT'])
def edit_user(id):
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)
    
    #extracting the variable
    username = the_data['username']
    email = the_data['email']
    password = the_data['password']
    birthday = the_data['birthday']

    # Constructing the query
    query = '''update users SET username = "{}", 
    email = "{}", password = "{}", birthday = "{}" where id = {}'''.format(username, email, password, birthday, id)
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

#get the info on a specific user
@users.route('/users/<id>', methods=['GET'])
def get_user (id):
    query = 'SELECT * FROM users WHERE id = ' + id
    #internal flask logging
    current_app.logger.info("-----------------------")
    current_app.logger.info("")
    current_app.logger.info(query)
    current_app.logger.info("")
    current_app.logger.info("-----------------------")

    #do the get
    cursor = db.get_db().cursor()
    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)

# get saved logs
@users.route('/users/<id>/saves', methods=['GET'])
def get_saved(id):
    cursor = db.get_db().cursor()
    cursor.execute(f'select log_id, content from user_saved_logs\
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

# get owned groves 
@users.route('/users/<id>/groves/owned', methods=['GET'])
def get_groves_owned(id):
    cursor = db.get_db().cursor()
    query = '''select name, description, log_lists.id from log_lists join user_log_list_accesses on 
                   log_lists.id = user_log_list_accesses.log_list_id where user_id = {} and access = "creator"'''.format(id)
    cursor.execute(query)
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    return the_response

# get accessible groves 
@users.route('/users/<id>/groves/access', methods=['GET'])
def get_groves_access(id):
    cursor = db.get_db().cursor()
    query = '''select name, description, log_lists.id, user_log_list_accesses.access from log_lists join user_log_list_accesses on 
                   log_lists.id = user_log_list_accesses.log_list_id where user_id = {}'''.format(id)
    cursor.execute(query)
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    return the_response

# get follows
@users.route('/users/<id>/follows', methods=['GET'])
def get_follows(id):
    cursor = db.get_db().cursor()
    cursor.execute(f'''select username, user_id from user_follows_users join users on user_follows_users.user_id = users.id 
                   where follower_id = {id};''')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    return the_response

# get a user's following feed
@users.route('/users/<id>/feed/following', methods=['GET'])
def get_following(id):
    cursor = db.get_db().cursor()
    cursor.execute('''
select title, content, rating, logs.created_at, username, enterprise_id from
                    logs join users on logs.created_by = users.id
                    join log_lists on logs.log_list_id = log_lists.id

                   where created_by in (select user_id from user_follows_users where follower_id = {})
                   or log_lists.category_id in (select category_id from user_follows_categories where user_id = {})

                   order by logs.created_at desc limit 50;'''.format(id, id))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    return the_response

# get a user's home feed
@users.route('/users/<id>/feed/home', methods=['GET'])
def get_home(id):
    cursor = db.get_db().cursor()
    cursor.execute('''select logs.id as log_id, title, content, rating, logs.created_at, users.username, enterprise_id, log_lists.id as grove_id from logs join log_lists on
    logs.log_list_id=log_lists.id join user_log_list_accesses on
        log_lists.id=user_log_list_accesses.log_list_id join users on logs.created_by = users.id where
                                                    user_log_list_accesses.user_id = {};'''.format(id))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    return the_response

# follow user
@users.route('/users/<id>/follows', methods=['POST'])
def follow_user(id):
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)
    
    #extracting the variable
    user_id = the_data['user_id']

    # Constructing the query
    query = 'insert into user_follows_users (follower_id, user_id) values ("'
    query += str(id) + '", "'
    query += str(user_id) + '")'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

# unfollow user
@users.route('/users/<id>/follows', methods=['DELETE'])
def unfollow_user(id):
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)
    
    #extracting the variable
    user_id = the_data['user_id']

    # Constructing the query
    query = 'delete from user_follows_users where follower_id = {} AND user_id = {}'.format(id, user_id)
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

#delete a user
@users.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    query = 'delete from users where id = {}'.format(id)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'