from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db

groves = Blueprint('groves', __name__)

# create grove
@groves.route('/groves', methods=['POST'])
def create_grove():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)
    
    #extracting the variable
    name = the_data['name']
    description = the_data['description']
    is_private = the_data['is_private']
    user_id = the_data['user_id']

    # Constructing the query
    query = 'insert into log_lists (name, description, is_private) values ("'
    query += name + '", "'
    query += description + '", "'
    query += str(is_private) + '")'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    # inserting user as creator of grove

    query = 'select * from log_lists order by created_at desc limit 1'
    cursor.execute(query)

    
    query = 'insert into user_log_list_accesses (user_id, log_list_id, access_id) values ("'
    query += str(user_id) + '", "'
    query += str(cursor.fetchall()[0][0]) + '", "'
    query += '1")'

    # executing and committing the insert statement 
    cursor.execute(query)
    db.get_db().commit()


    return 'Success!'

# edit grove
@groves.route('/groves/<id>', methods=['PUT'])
def edit_grove(id):
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)
    
    #extracting the variable
    name = the_data['name']
    description = the_data['description']
    is_private = the_data['is_private']
    if(not is_private):
        category_id = the_data['category_id']
        query = '''UPDATE log_lists SET name = {}, description = {}, is_private = 0, category_id = {} WHERE id={}
        
        
        '''.format(name, description, category_id, id)
        
    query = 'UPDATE log_lists SET name = "{}", description = "{}" where id = {}'.format(name, description, id)

    current_app.logger.info("-----------------------")
    current_app.logger.info("")
    current_app.logger.info(query)
    current_app.logger.info("")
    current_app.logger.info("-----------------------")

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return 'Success!'

# get all users and their access levels for a grove
@groves.route('/groves/<id>/accesses', methods=['GET'])
def get_grove_accessses (id):
    
    query = 'SELECT u.user_id, a.name as access_type FROM user_log_list_accesses u JOIN access_types a ON u.access_id = a.id WHERE u.log_list_id = ' + str(id)
    current_app.logger.info(query)
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)

# get logs
@groves.route('/groves/<id>', methods=['GET'])
def get_grove_logs (id):
    
    query = 'SELECT id, title, content, rating, created_at FROM logs WHERE log_list_id = ' + str(id)
    current_app.logger.info(query)
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)

# grant a new user access to a grove
@groves.route('/groves/<id>/accesses', methods=['POST'])
def grant_access_to_grove(id):
    
    # Collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)
    
    # Extracting the variables
    user_id = the_data['user_id']
    access_type = the_data['access_type']

    current_app.logger.info("-----------------------")
    current_app.logger.info("")
    current_app.logger.info(the_data)
    current_app.logger.info("")
    current_app.logger.info("-----------------------")
    
    # Get the access_id from access_types table based on the provided access_type
    query_access_id = 'SELECT id FROM access_types WHERE name = "{}"'.format(access_type)
    
    cursor = db.get_db().cursor()
    cursor.execute(query_access_id)
    access_id = cursor.fetchall()[0][0]
    
    # Constructing the query
    query_insert_access = '''
        INSERT INTO user_log_list_accesses (user_id, log_list_id, access_id)
        VALUES ({}, {}, {})
    '''.format(user_id, id, access_id)

    current_app.logger.info(query_insert_access)

    # Executing and committing the insert statement 
    cursor.execute(query_insert_access)
    db.get_db().commit()

    return 'Access granted successfully'

# change a user's access level in a grove
@groves.route('/groves/<id>/accesses', methods=['PUT'])
def change_access_level(id):
    
    # Collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)
    
    # Extracting the variables
    user_id = the_data['user_id']
    new_access_type = the_data['access_type']
    
    # Get the access_id from access_types table based on the provided new_access_type
    query_access_id = 'SELECT id FROM access_types WHERE name = "{}"'.format(new_access_type)
    
    cursor = db.get_db().cursor()
    cursor.execute(query_access_id)
    access_id = cursor.fetchall()[0][0]
    
    # Constructing the query
    query_update_access = '''UPDATE user_log_list_accesses SET access_id = {} WHERE log_list_id = {} AND user_id = {}'''.format(str(access_id), str(id), str(user_id))

    current_app.logger.info(query_update_access)

    # Executing and committing the update statement 
    cursor.execute(query_update_access)
    db.get_db().commit()

    return 'Access level changed successfully'

# deny a user access to a grove
@groves.route('/groves/<id>/accesses', methods=['DELETE'])
def deny_access(id):
    
    # Collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)
    
    # Extracting the variables
    user_id = the_data['user_id']
    
    # Constructing the query
    query_delete_access = (
        'DELETE FROM user_log_list_accesses '
        f'WHERE log_list_id = {id} AND user_id = {user_id}'
    )

    current_app.logger.info(query_delete_access)

    # Executing and committing the delete statement 
    cursor = db.get_db().cursor()
    cursor.execute(query_delete_access)
    db.get_db().commit()

    return 'Removed user from grove successfully'

@groves.route('groves/<id>', methods=['DELETE'])
def delete_grove(id):

    query = (
        'DELETE FROM log_lists WHERE id = ' + str(id)
    )

    current_app.logger.info(query)

    # Executing and committing the delete statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return 'Deleted grove successfully'