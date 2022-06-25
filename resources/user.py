import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='This is a required field.')
  
    parser.add_argument('password', type=str, required=True, help='This is a required field.')
    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message": "That name is already taken"}, 400
        user = UserModel(**data)
        user.save_to_db()
        return {"message": "User created successfully"}, 201
        
