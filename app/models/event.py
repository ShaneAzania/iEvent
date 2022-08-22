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
        self.time = db_data['time']
        self.attendee_limit = db_data['attendee_limit']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user_id = db_data['user_id']
        self.user = None
        self.attendees = []

    @classmethod 
    def save(cls,event):
        query = "INSERT INTO events(name,information,location,time,attendee_limit,user_id) VALUES (%(name)s, %(information)s, %(location)s, %(time)s,%(attendee_limit)s,%(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, event)

    @classmethod 
    def get_all_events(cls):
        query = "SELECT * FROM events LEFT JOIN users ON events.user_id = users.id ORDER BY time ASC;"
        results = connectToMySQL(cls.db).query_db(query)
        all_events = []
        for row in results:
            # create 'this_event' object
            this_event = cls(row)
            # create user object and set 'event.user' equal to this user object
            this_event.user = user.User.get_one({'id':row['users.id']})
            #  append this event object to 'all_events' list
            all_events.append(this_event)
        return all_events 
    @classmethod 
    def get_all_events_future(cls):
        query = "SELECT * FROM events LEFT JOIN users ON events.user_id = users.id WHERE time > now() ORDER BY time ASC;"
        results = connectToMySQL(cls.db).query_db(query)
        all_events = []
        for row in results:
            # create 'this_event' object
            this_event = cls(row)
            # create user object and set 'event.user' equal to this user object
            this_event.user = user.User.get_one({'id':row['users.id']})
            #  append this event object to 'all_events' list
            all_events.append(this_event)
        return all_events 
    @classmethod 
    def get_all_events_past(cls):
        # get events with user (one to many)
        query = "SELECT * FROM events LEFT JOIN users ON events.user_id = users.id WHERE time < now() ORDER BY time ASC;"
        results = connectToMySQL(cls.db).query_db(query)
        all_events = []
        for row in results:
            # create 'this_event' object
            this_event = cls(row)
            # create user object and set 'event.user' equal to this user object
            this_event.user = user.User.get_one({'id':row['users.id']})
            #  append this event object to 'all_events' list
            all_events.append(this_event)
        return all_events 

    @classmethod 
    def get_one_event(cls, event):
        query = " SELECT * FROM events WHERE events.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,event)
        this_event = cls(results[0])
        # get event creator user object
        this_event.user = user.User.get_one({'id': this_event.user_id})

        # GET ATTENDEES for this event (many to many)
        query_attendees = ""\
            "SELECT * FROM events "\
            "LEFT JOIN events_with_attendees ON events.id = events_with_attendees.event_id "\
            "LEFT JOIN users ON events_with_attendees.user_id = users.id "\
            "WHERE events.id = %(id)s "\
            "ORDER BY time ASC;"
        results_attendees = connectToMySQL(cls.db).query_db(query_attendees, event)
        for attendee in results_attendees:
            # arrange data
            data = {
                'id': attendee['users.id'],
                'first_name': attendee['first_name'],
                'last_name': attendee['last_name'],
                'email': attendee['email'],
                'password': attendee['password'],
                'created_at': attendee['users.created_at'],
                'updated_at': attendee['users.updated_at']
            }
            # create user object
            this_user = user.User(data)

            #  append this user object to 'attendees' list
            this_event.attendees.append(this_user)
        # END GET ATTENDEES

        return this_event

    @classmethod 
    def update(cls,event):
            query = "UPDATE events SET name=%(name)s,information=%(information)s,location=%(location)s,time=%(time)s, attendee_limit=%(attendee_limit)s,updated_at=NOW() WHERE id = %(id)s;"
            return connectToMySQL(cls.db).query_db(query, event)

    @classmethod 
    def delete(cls,data):
        # delete messages associated with this event
        query = " DELETE FROM messages WHERE event_id=%(event_id)s;"
        connectToMySQL(cls.db).query_db(query, data)
        # delete events_with_attendees pair
        query = " DELETE FROM events_with_attendees WHERE event_id=%(event_id)s;"
        connectToMySQL(cls.db).query_db(query, data)
        # delete event
        query = " DELETE FROM events WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod 
    def add_attendee(cls,event):
        # check the current attendee limit
        query = "SELECT * FROM events WHERE id = %(event_id)s;"
        result = connectToMySQL(cls.db).query_db(query, event)
        this_event = cls.get_one_event(result[0])
        attendee_limit = this_event.attendee_limit
        # check the current number of attendees
        query = "SELECT * FROM events_with_attendees WHERE event_id = %(event_id)s;"
        result = connectToMySQL(cls.db).query_db(query, event)
        attendee_quantity = len(result)

        print('ATTENDEE LIMIT:', attendee_limit)
        print('ATTENDEE QUANTITY:', attendee_quantity)

        # check if this user is a current attendee
        query = "SELECT * FROM events_with_attendees WHERE event_id = %(event_id)s AND user_id = %(user_id)s;"
        result = connectToMySQL(cls.db).query_db(query, event)
        if result:
            return False
        elif attendee_limit <= attendee_quantity:
            flash('Sorry, attendee limit reached.')
            return False
        elif attendee_limit > attendee_quantity:
            # if this user is not a current attendee and attendee_limit is not reached, create the row
            query = "INSERT INTO events_with_attendees(event_id, user_id) VALUES (%(event_id)s, %(user_id)s);"
            connectToMySQL(cls.db).query_db(query, event)
            # check the current number of attendees after the insert into the database
            query = "SELECT * FROM events_with_attendees WHERE event_id = %(event_id)s;"
            result = connectToMySQL(cls.db).query_db(query, event)
            print('ATTENDEE QUANTITY AFTER INSERT INTO DATABASE:', len(result))
            return 
    @classmethod 
    def delete_attendee(cls,event):
        # check if pair exists
        query = "SELECT * FROM events_with_attendees WHERE event_id = %(event_id)s AND user_id = %(user_id)s;"
        result = connectToMySQL(cls.db).query_db(query, event)
        if result:
            # if pair exist, delete it
            query = "DELETE FROM events_with_attendees WHERE event_id = %(event_id)s AND user_id = %(user_id)s;"
            return connectToMySQL(cls.db).query_db(query, event)
        else:
            print('PAIR DOES NOT EXIST EXIST')
            return



# ************************** validation 
# time validation will need updated and we need to add attendees etc. 

    @staticmethod 
    def validate_event(event):
        is_valid = True 
        if len(event['name']) < 2:
            is_valid = False
            flash("Evnet name must be at least 2 characters","event")
        if len(event['location']) < 2:
            is_valid = False
            flash("Location must be at least 2 characters","event")
        if len(event['time']) < 4:
            is_valid = False
            flash("Time must be at least 4 characters","event")
        if int(event['attendee_limit']) < 1:
            is_valid = False
            flash("Attendee Limit Must be greater than 0","event")
        # if len(event['attendees']) < 1:
        #     is_valid = False
        #     flash("Attendees must be at greater than 1","event") 
        return is_valid  
