from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.blog import Blog
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
        self.blogs = []
        
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
    
    @classmethod 
    def get_one_user_with_blogs(cls, data):
        query = """
            SELECT * FROM users LEFT JOIN blogs ON
            blogs.user_id = users.id WHERE users.id = %(id)s;
        """
        results = connectToMySQL('blogs_schema').query_db(query, data)
        one_user = cls(results[0])
        for row in results:
            blog_data = {
                "id": row['blogs.id'],
                "user_id": row["user_id"],
                "name": row["name"],
                "topic": row['topic'],
                "description": row['description'],
                "created_at": row['blogs.created_at'],
                "updated_at": row['blogs.updated_at']
            }
            one_blog = Blog(blog_data)
            one_user.blogs.append(one_blog)
        return one_user