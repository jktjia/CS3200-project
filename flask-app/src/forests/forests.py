from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


forests = Blueprint('forests', __name__)

# get groves from forest
@forests.route('/forests/<id>', methods=['GET'])
def forest_get_groves (id):
    query = 'SELECT id, name, description, created_at FROM log_lists WHERE category_id = ' + str(id)
    current_app.logger.info(query)
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)

# get list of forests
@forests.route('/forests', methods=['GET'])
def forests_get_categories ():
    query = 'select * from categories order by id'
    current_app.logger.info(query)
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)