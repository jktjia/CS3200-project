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
    query += content + '", '
    query += str(rating) + ', "'
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
    content = the_data['content']

    # Constructing the query
    query = 'insert into comments (user_id, content, log_id) values ("'
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


@logs.route('/logs/toggle_like', methods=['POST'])
def toggle_like_log():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info("hi")
    current_app.logger.info(the_data)
    
    #extracting the variable
    user_id = the_data['user_id']
    log_id = the_data['log_id']

    likes_or_not = get_liked_or_not(log_id,user_id).json
    current_app.logger.info(likes_or_not)
    if likes_or_not[0] == "Unlike":
        query = f'DELETE from user_liked_logs WHERE log_id =  {log_id} and user_id = {user_id}'
        current_app.logger.info(query)

        # executing and committing the insert statement 
        cursor = db.get_db().cursor()
        cursor.execute(query)
        db.get_db().commit()    
        return "Unliked!"
    else:
        query = 'insert into user_liked_logs (user_id, log_id) values ("'
        query += str(user_id) + '", "'
        query += str(log_id) + '")'
        current_app.logger.info(query)

        # executing and committing the insert statement 
        cursor = db.get_db().cursor()
        cursor.execute(query)
        db.get_db().commit()
        return 'Liked!'



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
    query = 'SELECT logs.*, users.username FROM logs join users on logs.created_by = users.id WHERE logs.id = ' + id
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
    # current_app.logger.info(the_data)
    return jsonify(json_data)

#get log comments
@logs.route('/logs/<id>/comment', methods=['GET'])
def get_comments (id):
    query = 'SELECT comments.id, content, log_id, username FROM comments JOIN users ON comments.user_id = users.id WHERE log_id = ' + str(id)
    cursor = db.get_db().cursor()
    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)

#get log comments
@logs.route('/logs/<id>/comment/count', methods=['GET'])
def get_comment_count (id):
    query = 'SELECT COUNT(*) as comment_count FROM comments WHERE log_id = ' + str(id)
    cursor = db.get_db().cursor()
    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)

#get log number of likes
@logs.route('/logs/<id>/like', methods=['GET'])
def get_likes (id):
    query = 'SELECT COUNT(*) as like_count FROM user_liked_logs WHERE log_id = ' + str(id)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)

#get whether or not user has liked a given log
@logs.route('/logs/<log_id>/like/<user_id>', methods=['GET'])
def get_liked_or_not(log_id,user_id):
    query = f'''SELECT COUNT(*) as like_count
      FROM user_liked_logs WHERE log_id = {log_id} and user_id = {user_id}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    value = the_data[0][0]
    current_app.logger.info('value is' + str(value))
    json_data.append("Like") if value == 0 else json_data.append("Unlike")
    # current_app.logger.info(return_value)
    # return return_value
    # for row in the_data:
    #     json_data.append(dict(zip(column_headers, row)))
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
def delete_comment(id):
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
def delete_like(id):
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
def delete_save(id):
    # Constructing the query
    query = 'DELETE from user_saved_logs WHERE log_id = ' + str(id)
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

# Get the most liked log in a category
@logs.route('/logs/stats/most-liked/<category_id>', methods=['GET'])
def get_most_liked(category_id):
    query = 'SELECT logs.id, logs.title, COUNT(user_liked_logs.log_id) AS like_count FROM logs ' \
            'JOIN log_lists ON logs.log_list_id = log_lists.id JOIN user_liked_logs ON logs.id = ' \
            'user_liked_logs.log_id WHERE log_lists.category_id = %s GROUP BY logs.id ' \
            'ORDER BY like_count DESC LIMIT 1'
    values = (category_id)
    cursor = db.get_db().cursor()
    cursor.execute(query, values)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)

# Get the average rating of logs in a category
@logs.route('/logs/stats/avg-rating/<category_id>', methods=['GET'])
def get_avg_rating(category_id):
    query = 'SELECT AVG(logs.rating) as average_rating FROM logs JOIN log_lists ON ' \
            'logs.log_list_id = log_lists.id WHERE log_lists.category_id = %s'
    values = (category_id)
    cursor = db.get_db().cursor()
    cursor.execute(query, values)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)

# Retrieve top 5 logs in a specific category based on likes
@logs.route('/logs/stats/top-five/<category_id>', methods=['GET'])
def get_top_five(category_id):
    query = 'SELECT logs.id, logs.content, logs.rating, logs.title, COUNT(user_liked_logs.log_id) AS like_count ' \
            'FROM logs JOIN log_lists ON logs.log_list_id = log_lists.id LEFT JOIN ' \
            'user_liked_logs ON logs.id = user_liked_logs.log_id WHERE log_lists.category_id = %s ' \
            'GROUP BY logs.id ORDER BY like_count DESC LIMIT 5'
    values = (category_id)
    cursor = db.get_db().cursor()
    cursor.execute(query, values)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)