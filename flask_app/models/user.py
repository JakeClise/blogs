from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.t_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @staticmethod
    def validate_register(user):
        is_valid = True
        if len(user['first_name']) < 2:
            flash("First Name must be greater than 2 characters!")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last Name must be greater than 2 characters!")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be greater than 8 characters!")
            is_valid = False
        if user['password'] != user['confpassword']:
            flash("Passwords do not match!")
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_login():
        pass

    @classmethod
    def save_user(cls, data):
        query = """
            INSERT INTO users (first_name, last_name, email, password) 
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """
        return connectToMySQL('blogs_schema').query_db(query, data)
    
    @classmethod
    def get_user_by_email(cls, data):
        query = """
            SELECT * FROM users WHERE email = %(email)s;
        """
        result = connectToMySQL('blogs_schema').query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_user_by_id(cls, data):
        query = """
            SELECT * FROM users WHERE id = %(id)s;
        """
        result = connectToMySQL('blogs_schema').query_db(query, data)
        return cls(result[0])