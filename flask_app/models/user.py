from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']

    @classmethod
    def get_user_by_id(cls, id):
        data = {
            'id' : id
        }
        query = """SELECT * FROM users WHERE id = %(id)s;"""
        results = connectToMySQL(DATABASE).query_db( query, data )
        if len(results) < 0:
            return False
        return cls(results[0])
    
    @classmethod
    def get_user_by_email(cls, data):
        # print(f"DATA>>{data}")
        query = """SELECT * FROM users WHERE email = %(email)s;"""
        results = connectToMySQL(DATABASE).query_db( query, data )
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def save(cls, data):
        query = """INSERT INTO users (username, email, password) VALUES (%(username)s, %(email)s, %(password)s);"""        
        user_id = connectToMySQL(DATABASE).query_db( query, data )
        return user_id
    
    
    @classmethod
    def check_user(cls, data):
        is_user = False
        query = """SELECT * FROM users WHERE users.email = %(email)s;"""
        user_id = connectToMySQL(DATABASE).query_db( query, data )
        if user_id:
            is_user = True
            flash('User is already registered!', 'email')
        return is_user
    
    @staticmethod
    def validate(data):
        is_valid = True
        if len(data['username']) < 3:
            is_valid = False
            flash('Username must be at least 3 characters', 'username')
        if not EMAIL_REGEX.match(data['email']):
            flash('Invalid email address!', 'email')
            is_valid = False
        if len(data['password']) < 8:
            is_valid = False
            flash('Password must be at least 8 characters!', 'password')
        if not data['password'] == data['confirm_password']:
            is_valid = False
            flash('Passwords must match!', 'password')
        return is_valid