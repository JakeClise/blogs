from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

class Blog:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.name = data['name']
        self.topic = data['topic']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None

    @staticmethod
    def validate_blog(blog):
        is_valid = True
        if len(blog['name']) < 4:
            flash("Blog name must be at least 4 characters")
            is_valid = False
        if len(blog['topic']) < 4: 
            flash("Blog topic must be at least 4 characters")
            is_valid = False
        if len(blog['description']) < 10:
            flash("Description must be at least 10 characters")
            is_valid = False
        if len(blog['description']) > 50:
            flash("Description cannot be more than 50 characters")
            is_valid = False
        return is_valid

    @classmethod
    def save_blog(cls, data):
        query = """
            INSERT INTO blogs (user_id, name, topic, description)
            VALUES (%(user_id)s, %(name)s, %(topic)s, %(description)s);
        """
        return connectToMySQL('blogs_schema').query_db(query,data)

    @classmethod
    def get_all_blogs_with_creator(cls):
        query = """
                SELECT * FROM blogs 
                JOIN users ON users.id =blogs.user_id;
        """
        results = connectToMySQL('blogs_schema').query_db(query)
        print(results)
        blogs = []
        for blog in results:
            blog_data = {
                "id": blog['id'],
                "user_id": blog["user_id"],
                "name": blog["name"],
                "topic": blog['topic'],
                "description": blog['description'],
                "created_at": blog['created_at'],
                "updated_at": blog['updated_at']
            }
            user_data = {
                "id": blog['users.id'],
                "first_name": blog['first_name'],
                "last_name": blog['last_name'],
                "email": blog['email'],
                "password": blog['password'],
                "created_at": blog['users.created_at'],
                "updated_at": blog['users.updated_at']
            }

            one_blog = cls(blog_data)
            one_blog.creator = user.User(user_data)
            blogs.append(one_blog)
        return blogs
    
    @classmethod
    def get_one_blog_with_user(cls, data):
        query = """
            SELECT * FROM blogs JOIN users ON blogs.user_id = users.id 
            WHERE blogs.id = %(id)s;
        """
        results = connectToMySQL('blogs_schema').query_db(query, data)
        one_blog = cls(results[0])
        
        user_data = {
            "id": results[0]['users.id'],
            "first_name": results[0]['first_name'],
            "last_name": results[0]['last_name'],
            "email": results[0]['email'],
            "password": results[0]['password'],
            "created_at": results[0]['users.created_at'],
            "updated_at": results[0]['users.updated_at']
        }

        one_blog.creator = user.User(user_data)
        return one_blog

    @classmethod
    def update_blog(cls, data):
        query = """
            UPDATE blogs SET name = %(name)s, topic = %(topic)s, description = %(description)s
            WHERE blogs.id = %(id)s;
        """
        return connectToMySQL('blogs_schema').query_db(query, data)
    
    @classmethod
    def delete_blog(cls, data):
        query = "DELETE FROM blogs WHERE blogs.id = %(id)s;"
        return connectToMySQL('blogs_schema').query_db(query, data)