from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


enterprises = Blueprint('enterprise', __name__)

# Add a new enterprise in the db
@enterprises.route('/enterprise', methods=['POST'])
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
@enterprises.route('/enterprise/<id>', methods=['GET'])
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
@enterprises.route('/enterprise/<id>', methods=['PUT'])
def update_enterprise_detail (id):
    the_data = request.json
    current_app.logger.info(the_data)
    
    #extracting the variable
    name = the_data['name']
    
    query = f'UPDATE enterprises SET name = {name} WHERE id = ' + str(id)
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
@enterprises.route('/enterprise/<id>', methods=['DELETE'])
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
@enterprises.route('/enterprise/<id>/card', methods=['POST'])
def add_enterprise_card (id):
    
    # collecting data from the request object 
    card_data = request.json
    current_app.logger.info(card_data)
    
    #extracting the variable
    number = card_data['number']
    security_code = card_data['security_code']
    expiration = card_data['expiration']
    first_name = card_data['first_name']
    last_name = card_data['last_name']
    
    query = 'INSERT INTO credit_cards (enterprise_id number, security_code, expiration, first_name, last_name) VALUES (%s, %s, %s, %s, %s, %s)'
    values = (id, number, security_code, expiration, first_name, last_name)
    cursor = db.get_db().cursor()
    cursor.execute(query, values)
    db.get_db().commit()
        
    return 'Added card to enterprise successfully!'

# Add card to enterprise
@enterprises.route('/enterprise/<id>/card', methods=['GET'])
def add_enterprise_card (id):
    query = 'SELECT * FROM credit_cards WHERE enterprise_id = ' + str(id)
    current_app.logger.info(query)
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)
   
# Remove card from enterprise
# Should it be /enterprise/<enterprise_id>/card/<card_id>???
@enterprises.route('/enterprise/card/<id>', methods=['DELETE'])
def remove_enterprise_card (id):
    delete_query = 'DELETE FROM credit_cards WHERE  credit_card_id = %s'
    values = (id)
    cursor = db.get_db().cursor()
    cursor.execute(delete_query, values)

    db.get_db().commit()

    return 'Card removed successfully!'


# Add a user to an enterprise
@enterprises.route('/enterprise/<id>/user/<user_id>', methods=['POST'])
def add_user_to_enterprise(id, user_id):
    the_data = request.json
    current_app.logger.info(the_data)
    
    # Update user's enterprise_id
    update_query = 'UPDATE users SET enterprise_id = %s WHERE id = %s'
    cursor = db.get_db().cursor()
    values = (id, user_id)
    cursor.execute(update_query, values)
    db.get_db().commit()

    return 'User added to enterprise successfully!'


# Remove user from enterprise
@enterprises.route('/enterprise/<id>/user/<user_id>', methods=['DELETE'])
def remove_user_from_enterprise(id, user_id):
    the_data = request.json
    current_app.logger.info(the_data)
    
    update_query = 'UPDATE users SET enterprise_id = NULL WHERE id = %s AND enterprise_id = %s'
    cursor = db.get_db().cursor()
    values = (user_id, id)
    cursor.execute(update_query, values)
    db.get_db().commit()

    return 'User removed from enterprise successfully!'

# Get forests of a specific enterpise
@enterprises.route('/enterprise/<id>/forests', methods=['GET'])
def get_enterprise_forests(id):
    the_data = request.json
    current_app.logger.info(the_data)
    
    query = 'SELECT categories.* FROM categories ' \
            'JOIN enterprise_categories ON categories.id = enterprise_categories.category_id ' \
            'WHERE enterprise_categories.enterprise_id = %s'
    values = (id,)
    cursor = db.get_db().cursor()
    cursor.execute(query, values)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)

@enterprises.route('/enterprise/<enterprise_id>/forests/<forest_id>', methods=['GET'])
def get_enterprise_category(enterprise_id, forest_id):
    the_data = request.json
    current_app.logger.info(the_data)
    
    query = 'SELECT categories.* FROM categories ' \
            'JOIN enterprise_categories ON categories.id = enterprise_categories.category_id ' \
            'WHERE enterprise_categories.enterprise_id = %s AND categories.id = %s'
    values = (enterprise_id, forest_id)
    
    cursor = db.get_db().cursor()
    cursor.execute(query, values)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)


@enterprises.route('/enterprise/<enterprise_id>/forests/<forest_id>', methods=['POST'])
def add_forest_to_enterprise(enterprise_id, forest_id):
    the_data = request.json
    current_app.logger.info(the_data)
    
    query = 'INSERT INTO enterprise_categories (enterprise_id, category_id) VALUES (%s, %s)'
    values = (enterprise_id, forest_id)
    
    cursor = db.get_db().cursor()
    cursor.execute(query, values)
    db.get_db().commit()
    return 'Forest added to enterprise successfully!'

@enterprises.route('/enterprise/<enterprise_id>/forests/<forest_id>', methods=['DELETE'])
def remove_forest_from_enterprise(enterprise_id, forest_id):
    the_data = request.json
    current_app.logger.info(the_data)
    
    query = 'DELETE FROM enterprise_categories WHERE enterprise_id = %s AND category_id = %s'
    
    values = (enterprise_id, forest_id)
    cursor = db.get_db().cursor()
    cursor.execute(query, values)
    db.get_db().commit()
    return 'Forest removed from enterprise successfully!'

@enterprises.route('/enterprise/search/logs', methods=['GET'])
def get_logs_keyword():
    the_data = request.json
    current_app.logger.info(the_data)
    
    keyword = the_data['keyword'] # Unsure if this is the correct way
    query = 'SELECT * FROM logs WHERE content LIKE %s'
    values = ('%' + keyword + '%',)
    cursor = db.get_db().cursor()
    
    cursor.execute(query, values)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)

@enterprises.route('/enterprise/search/groves', methods=['GET'])
def get_categories_keyword():
    the_data = request.json
    current_app.logger.info(the_data)
    
    keyword = the_data['keyword'] # Unsure if this is the correct way
    query = 'SELECT * FROM categories WHERE topic LIKE %s'
    values = ('%' + keyword + '%',)
    
    cursor = db.get_db().cursor()
    cursor.execute(query, values)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)
