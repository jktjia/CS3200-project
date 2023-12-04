from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db



enterprises = Blueprint('enterprises', __name__)

# Add a new enterprise in the db
@enterprises.route('/enterprises', methods=['POST'])
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
    
    return 'Added enterprise successfully!'

# Get enterprise information
@enterprises.route('/enterprises/<id>', methods=['GET'])
def get_enterprise_detail (id):
    query = 'SELECT id, name FROM enterprises WHERE id = ' + str(id)
    current_app.logger.info(query)
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)

# Update enterprise information
@enterprises.route('/enterprises/<id>', methods=['PUT'])
def update_enterprise_detail (id):
    the_data = request.json
    current_app.logger.info(the_data)
    
    #extracting the variable
    name = the_data['name']
    
    query = f'UPDATE enterprises SET name = {name} WHERE = ' + str(id)
    current_app.logger.info(query)
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    return 'Updated enterprise successfully!'

# Delete enterprise
@enterprises.route('/enterprises/<id>', methods=['DELETE'])
def remove_enterprise_detail (id):
    query = 'DELETE FROM enterprises WHERE id = ' + str(id)
    current_app.logger.info(query)
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    return 'Deleted enterprise successfully!'

# Add card to enterprise
@enterprises.route('/enterprises/<id>/card', methods=['POST'])
def add_enterprise_card (id):
    
    # collecting data from the request object 
    card_data = request.json
    current_app.logger.info(card_data)
    
    #extracting the variable
    card_data = request.json
    number = card_data['number']
    security_code = card_data['security_code']
    expiration = card_data['expiration']
    first_name = card_data['first_name']
    last_name = card_data['last_name']
    
    query = 'INSERT INTO credit_cards (number, security_code, expiration, first_name, last_name) VALUES (%s, %s, %s, %s, %s)'
    values = (number, security_code, expiration, first_name, last_name)
    cursor = db.get_db().cursor()
    cursor.execute(query, values)
    credit_card_id = cursor.lastrowid

    # Linking credit card to enterprise
    link_query = 'INSERT INTO enterprise_credit_cards (enterprise_id, credit_card_id) VALUES (%s, %s)'
    values = (id, credit_card_id)
    cursor.execute(link_query, values)
    db.get_db().commit()
        
    return 'Added card to enterprise successfully!'
   
# Remove card from enterprise
# Should it be /enterprise/<enterprise_id>/card/<card_id>???
@enterprises.route('/enterprises/<id>/card', methods=['DELETE'])
def remove_enterprise_card (id):
    
    card_id = request.json['card_id'] # UNSURE HOW TO FORMAT TO GET IT FROM THIS JSON REQUEST

    delete_query = 'DELETE FROM enterprise_credit_cards WHERE enterprise_id = %s AND credit_card_id = %s'
    values = (id, card_id)
    cursor = db.get_db().cursor()
    cursor.execute(delete_query, values)

    card_delete_query = 'DELETE FROM credit_cards WHERE id = %s'
    values = (card_id,)
    cursor.execute(card_delete_query, values)

    db.get_db().commit()

    return 'Card removed successfully!'


# Add a user to an enterprise
@enterprises.route('/enterprises/<id>/user/<user_id>', methods=['POST'])
def add_user_to_enterprise(id, user_id):
    # Update user's enterprise_id
    update_query = 'UPDATE users SET enterprise_id = %s WHERE id = %s'
    cursor = db.get_db().cursor()
    values = (id, user_id)
    cursor.execute(update_query, values)
    db.get_db().commit()

    return 'User added to enterprise successfully!'


# Remove user from enterprise
@enterprises.route('/enterprises/<id>/user/<user_id>', methods=['DELETE'])
def remove_user_from_enterprise(id, user_id):
    
    update_query = 'UPDATE users SET enterprise_id = NULL WHERE id = %s AND enterprise_id = %s'
    cursor = db.get_db().cursor()
    values = (user_id, id)
    cursor.execute(update_query, values)
    db.get_db().commit()

    return 'User removed from enterprise successfully!'


# @enterprises.route('/enterprises/<id>/forests', methods=['GET'])
# def get_enterprise_forests(id):
#     return


# @enterprises.route('/enterprises/<enterprise_id>/forests/<forest_id>', methods=['POST'])
# def add_forest_to_enterprise(enterprise_id, forest_id):
#     return


# @enterprises.route('/enterprises/<enterprise_id>/forests/<forest_id>', methods=['DELETE'])
# def remove_forest_from_enterprise(enterprise_id, forest_id):
#     return 

# @enterprises.route('/enterprises/search/logs', methods=['GET'])
# def get_logs_keyword():
#     return

# @enterprises.route('/enterprises/search/groves', methods=['GET'])
# def get_groves_keyword():
#     return