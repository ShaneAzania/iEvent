from app.config.mysqlconnection import connectToMySQL
from flask import flash
from app.models import user, event

class Message: 
    db = "iSport"
    db_table = "messages"
    def __init__(self,db_data):
        self.id = db_data['id']
        self.message = db_data['message']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user_id = db_data['user_id']
        self.event_id = db_data['event_id']
        self.user = None
        self.event = None

    @classmethod 
    def create(cls,event):
        query = "INSERT INTO messages (message,user_id,event_id) VALUES (%(message)s, %(user_id)s, %(event_id)s);"
        return connectToMySQL(cls.db).query_db(query, event)

    @classmethod 
    def get_all_messages_for_event(cls,data):
        query = "SELECT * FROM messages "\
                "LEFT JOIN users ON messages.user_id = users.id "\
                "LEFT JOIN events ON messages.event_id = events.id "\
                "WHERE events.id = %(event_id)s "\
                "ORDER BY messages.created_at DESC;"
        results = connectToMySQL(cls.db).query_db(query,data)
        messages = []
        if not results:
            return False
        for row in results:
            # create message object
            message = cls(row)
            # collect user and event objects
            message.user = user.User.get_one({'id':row['users.id']})
            message.event = event.Event.get_one_event({'id': row['events.id']})
            # append this message object to messages list
            messages.append(message)
        return messages 
    @classmethod 
    def get_one_message(cls,data):
        query = "SELECT * FROM messages WHERE messages.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        row = results[0]
        # create message object
        message = cls(row)
        # collect user and event objects
        message.user = user.User.get_one({'id':row['user_id']})
        message.event = event.Event.get_one_event({'id': row['event_id']})
        return message

    @classmethod 
    def update(cls,data):
            query = "UPDATE messages SET message=%(message)s,updated_at=NOW() WHERE id = %(id)s;"
            return connectToMySQL(cls.db).query_db(query, data)

    @classmethod 
    def delete(cls,data):
        # delete message
        query = " DELETE FROM messages WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    # ************************** validation 
    # time validation will need updated and we need to add attendees etc. 

    @staticmethod 
    def validate(event):
        is_valid = True 
        if len(event['message']) < 2:
            is_valid = False
            flash("Message must be longer","event")
        return is_valid  
       