from sqlite3 import dbapi2
from unittest import result
from app.config.mysqlconnection import connectToMySQL
from flask import flash
from app.models import user 

class Event: 
    db = "iSport"
    db_table = "events"
    def __init__(self,db_data):
        self.id = db_data['id']
        self.name = db_data['name']
        self.information = db_data['information']
        self.location = db_data['location']
        self.attendees = db_data['attendees']
        self.attendees_confirmed = db_data['attendees_confirmed']
        self.time = db_data['time']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user = None


    @classmethod 
    def save(cls,event):
        query = "INSERT INTO events(name,information,location,time,user_id) VALUES (%(name)s, %(information)s, %(location)s, %(time)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, event)

    @classmethod 
    def get_all_events(cls):
        query = " SELECT * FROM events;"
        results = connectToMySQL(cls.db).query_db(query)
        all_events = []
        for row in results:
            print (row['name'])
            all_events.append(cls(row) )
        return all_events 

    @classmethod 
    def get_one_event(cls, event):
        query = " SLECT * FROM events WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,event)
        return cls(results[0])

    # @classmethod 
    # def get_all_events_with_users(cls,data):
    #     query = "SELECT * FROM events JOIN users on events.user_id = users.id"
    #     results = connectToMySQL(cls.db).query_db(query,data)
    #     if len(results) == 0:
    #         return []
    #     else: 
    #         all_event_instances = []
    #         for current_event_dic in results: 
    #             event_instance = cls(current_event_dic)
    #             new_event_dic ={
    #                 "id": current_event_dic['users.id'],
    #                 "first_name": current_event_dic['first_name'],
    #                 "last_name": current_event_dic['last_name'],
    #                 "email": current_event_dic['email'],
    #                 "password": current_event_dic['password'],
    #                 "confirm_password": current_event_dic['confirm_password'],
    #                 "created_at": current_event_dic['users.created_at'],
    #                 "updated_at": current_event_dic['users.updated_at'],
    #             }
    #             user_instance = user.User(new_event_dic)
    #             event_instance.user = user_instance
    #             all_event_instances.append(event_instance)
    #         return all_event_instances

    @classmethod 
    def update(cls,event):
            query = "UPDATE events SET name=%(name)s,location=%(location)s,attendees=%(attendees)s,attendees_confirmed=%(attendees_confirmed)s,time=%(time)s,updated_at=NOW() WHERE id = %(id)s;"
            return connectToMySQL(cls.db).query_db(query, event)

    @classmethod 
    def destroy (cls,event):
        query = " DELETE FROM events WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query, event)

# ************************** validation 
# time validation will need updated and we need to add attendees etc. 

    @staticmethod 
    def validate_event(event):
        is_valid = True 
        if len(event['name']) < 2:
            is_valid = False
            flash("Evnet first name must be at least 2 characters","event")
        if len(event['information']) < 10:
            is_valid = False
            flash("Provide more information about this event","event")
        if len(event['location']) < 2:
            is_valid = False
            flash("Location must be at least 2 characters","event")
        if len(event['time']) < 4:
            is_valid = False
            flash("Time must be at least 4 characters","event")
        # if len(event['attendees']) < 1:
        #     is_valid = False
        #     flash("Attendees must be at greater than 1","event")
        return is_valid  
       