from sqlite3 import dbapi2
from unittest import result
from flask import flash
from app.assets.regex import EMAIL_REGEX
from app.config.mysqlconnection import connectToMySQL
from app.models.event import Event 

class User:
    db = 'isport'
    db_table = 'users'
    def __init__(self , db_data ):
        self.id = db_data['id']
        self.first_name = db_data['first_name']
        self.last_name = db_data['last_name']
        self.email = db_data['email']
        self.password = db_data['password']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
    # **********************************************************************************************************************************
    # create*****************************************************************
    @classmethod
    def create( cls , data ):
        query = "INSERT INTO " + cls.db_table + " ( first_name, last_name, email, password ) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s );"
        return connectToMySQL(cls.db).query_db( query, data)
    #**********************************************************************************************************************************
    #retreive*****************************************************************
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM " + cls.db_table + ";"
        result =  connectToMySQL(cls.db).query_db(query)
        users =[]
        for x in result:
            users.append(cls(x))
        return users
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM " + cls.db_table + " WHERE id = %(id)s;"
        result =  connectToMySQL(cls.db).query_db(query,data)
        if result: 
            return cls(result[0])
        else:
            print('Not in database')
            return result
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM " + cls.db_table + " WHERE email = %(email)s;"
        result = connectToMySQL(cls.db).query_db( query, data)

        if result:
            return cls(result[0])
        else:
            return result
    #**********************************************************************************************************************************
    #update*****************************************************************
    # first_name last_name email password age dojo_id
    @classmethod
    def update(cls,data):
        query = "UPDATE "+ cls.db_table +" SET first_name = '%(first_name)s', last_name = '%(last_name)s', email = '%(email)s', password = '%(password)s', updated_at = now() WHERE id = %(id)s;"
        connectToMySQL(cls.db).query_db( query, data)
    #**********************************************************************************************************************************
    #delete*****************************************************************
    @classmethod
    def delete (cls, data):
        query = "DELETE FROM " + cls.db_table + " WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db( query, data)
    #**********************************************************************************************************************************
    # validate*****************************************************************
    def validate_form(data):
        valid = True
        if 'first_name' in data and len(data['first_name']) < 2:
            valid = False
            flash('First name must be at least 3 characters long.')
        if 'last_name' in data and len(data['last_name']) < 2:
            valid = False
            flash('Last name must be at least 3 characters long.')
        if not EMAIL_REGEX.match(data['email']):
            valid = False
            flash('Please provide a valid email address (  example@email.com ).')
        if len(data['password']) < 8:
            valid = False
            flash('Password must be at least 8 characters long.')
        if 'password2' in data:
            if not data['password'] == data['password2']:
                valid = False
                flash('Passwords do not match.')
            elif len(data['password']) < 4:
                valid = False
                flash('Please enter a longer password.')
        return valid


