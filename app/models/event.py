from sqlite3 import dbapi2
from unittest import result
from app.config.mysqlconnection import connectToMySQL
from flask import flash
from app.models import user 

class Event: 
    db = "iSport"
    db_table = "events"
    def __init__(self,db_data):
        self.id = db_data ['id']
        self.name = db_data['name']
        self.location = db_data ['location']
        self.attendees = db_data ['attendees']
        self.attendees_confirmed = db_data ['attendees_confimred']
        self.time = db_data ['time']
        self.created_at = db_data ['created_at']
        self.updated_at = db_data ['updated_at']
        self.user = None

