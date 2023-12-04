from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


grove = Blueprint('grove', __name__)

# get logs from grove
@grove.route('/grove/<id>', methods=['GET'])
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


# get all users and their access levels for a grove
@grove.route('/grove/<id>/accesses', methods=['GET'])
def get_grove_accessses (id):
    
    query = 'SELECT u.user_id, a.name as access_type FROM user_log_list_accessses u JOIN access_types a ON u.access_id = a.id WHERE u.log_list_id = ' + str(id)
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
@grove.route('/grove/<id>/accesses', methods=['POST'])
def grant_access_to_grove(id):
    
    # Collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)
    
    # Extracting the variables
    user_id = the_data['user_id']
    access_type = the_data['access_type']
    
    # Get the access_id from access_types table based on the provided access_type
    query_access_id = 'SELECT id FROM access_types WHERE name = "{}"'.format(access_type)
    
    cursor = db.get_db().cursor()
    cursor.execute(query_access_id)
    access_id = cursor.fetchone()[0]
    
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
@grove.route('/grove/<id>/accesses', methods=['PUT'])
def change_access_level(id):
    
    # Collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)
    
    # Extracting the variables
    user_id = the_data['user_id']
    new_access_type = the_data['new_access_type']
    
    # Get the access_id from access_types table based on the provided new_access_type
    query_access_id = 'SELECT id FROM access_types WHERE name = ' + str(new_access_type)
    
    cursor = db.get_db().cursor()
    cursor.execute(query_access_id)
    access_id = cursor.fetchone()[0]
    
    # Constructing the query
    query_update_access = ''''
        UPDATE user_log_list_accesses
        SET access_id = {}
        WHERE log_list_id = {} AND user_id = {}
    '''.format(access_id, id, user_id)

    current_app.logger.info(query_update_access)

    # Executing and committing the update statement 
    cursor.execute(query_update_access)
    db.get_db().commit()

    return 'Access level changed successfully'

# deny a user access to a grove
@grove.route('/grove/<id>/accesses', methods=['DELETE'])
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

    return 'Access denied successfully'









