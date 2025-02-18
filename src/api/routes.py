"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Post, Comment, Likes, New, Tutorial
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

# @api.route('/signup', methods=['POST'])
# def signup():
#     data = request.get.json()

#     email = data.get('email')
#     username = data.get('username')
#     password = data.get('password')

#     if not email or not password or not username:
#         print("Falta introducir email/password/username")
#         return jsonify({"messsage": "Todos los campos son requeridos"}), 400

#     if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
#         print("El usuario ya existe")
#         return jsonify("message": "El usuario ya existe"), 400

#     hashed_password = generate_password_hash(password)
#     print("Contraseña hasheada correctamente")

#     new_user= User(
#         email=email,
#         username=username,
#         password=hashed_password
#     )