from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


logs = Blueprint('logs', __name__)

#create log
@logs.route('/logs', methods=['POST'])
def create_log():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)
    
    #extracting the variable
    title = the_data['title']
    content = the_data['content']
    rating = the_data['rating']
    log_list_id = the_data['grove']
    created_by = the_data['user']

    current_app.logger.info(title)

    # Constructing the query
    query = 'insert into logs (title, content, rating, created_by, log_list_id) values ("'
    query += title + '", "'
    query += content + '", "'
    query += str(rating) + '", "'
    query += str(created_by) + '", "'
    query += str(log_list_id) + '")'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

#comment log
@logs.route('/logs/<id>/comment', methods=['POST'])
def comment_log(id):
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)
    
    #extracting the variable
    user_id = the_data['user_id']
    content = the_data['contennt']

    # Constructing the query
    query = 'insert into comments (user_id, log_id, content) values ("'
    query += str(user_id) + '", "'
    query += content + '", "'
    query += str(id) + '")'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'


#like log
@logs.route('/logs/<id>/like', methods=['POST'])
def like_log(id):
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)
    
    #extracting the variable
    user_id = the_data['user_id']

    # Constructing the query
    query = 'insert into user_liked_logs (user_id, log_id) values ("'
    query += str(user_id) + '", "'
    query += str(id) + '")'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

#save log
@logs.route('/logs/<id>/save', methods=['POST'])
def save_log(id):
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)
    
    #extracting the variable
    user_id = the_data['user_id']

    # Constructing the query
    query = 'insert into user_saved_logs (user_id, log_id) values ("'
    query += str(user_id) + '", "'
    query += str(id) + '")'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

#get log
@logs.route('/logs/<id>', methods=['GET'])
def get_log (id):
    query = 'SELECT * FROM logs WHERE id = ' + id
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

#get log comments
@logs.route('/logs/<id>/comment', methods=['GET'])
def get_comments (id):
    query = 'SELECT * FROM comments WHERE log_id = ' + str(id)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)

#get log likes
@logs.route('/logs/<id>/like', methods=['GET'])
def get_comments (id):
    query = 'SELECT * FROM user_liked_logs WHERE log_id = ' + str(id)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)

#delete a log
@logs.route('/logs/<id>', methods=['DELETE'])
def delete_log(id):
    # Constructing the query
    query = 'DELETE from logs WHERE id = ' + str(id)
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

#delete comment
@logs.route('/logs/<id>/comment', methods=['DELETE'])
def delete_log(id):
    # Constructing the query
    query = 'DELETE from comments WHERE log_id = ' + str(id)
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

#delete like
@logs.route('/logs/<id>/like', methods=['DELETE'])
def delete_log(id):
    # Constructing the query
    query = 'DELETE from user_liked_logs WHERE log_id = ' + str(id)
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

#delete save
@logs.route('/logs/<id>/save', methods=['DELETE'])
def delete_log(id):
    # Constructing the query
    query = 'DELETE from user_saved_logs WHERE log_id = ' + str(id)
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'