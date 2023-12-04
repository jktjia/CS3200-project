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

#get the info on a specific user
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

#make a new log
@logs.route('/logs/<id>', methods=['PUT'])
def update_log():
    
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
