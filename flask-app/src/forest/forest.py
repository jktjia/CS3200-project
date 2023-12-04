from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


forest = Blueprint('forest', __name__)

# get groves from forest
@forest.route('/forest/<id>/groves', methods=['GET'])
def get_groves_forest (id):
    
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



