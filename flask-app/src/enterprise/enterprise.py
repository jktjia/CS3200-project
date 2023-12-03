from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db



enterprise = Blueprint('enterprise', __name__)

# Add a new enterprise in the db
@enterprise.route('/enterprise', methods=['POST'])
def add_new_enterprise():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)
    
    #extracting the variable
    name = the_data['name']
    
    # Constructing the query
    query = 'insert into enterprises (name) value ("'
    query += name + '")'
    current_app.logger.info(query)
    
    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

# Get enterprise information
@enterprise.route('/enterprise/<id>', methods=['GET'])
def get_enterprise_detail (id):
    
    query = 'SELECT id, name FROM enterprise WHERE id = ' + str(id)
    current_app.logger.info(query)
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)


# @enterprise.route('/enterprise/<id>/card', methods=['POST'])
# def add_enterprise_card (id):
    
#     # collecting data from the request object 
#     the_data = request.json
#     current_app.logger.info(the_data)
    
#     #extracting the variable
#     name = the_data['name']
    
#     # Constructing the query
#     query = 'insert into value ("'
#     query +=  + '")'
#     current_app.logger.info(query)
    
#     # executing and committing the insert statement 
#     cursor = db.get_db().cursor()
#     cursor.execute(query)
#     db.get_db().commit()
    
#     return 'Success!'