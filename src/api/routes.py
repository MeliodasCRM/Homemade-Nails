"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Post, Comment, Likes, New, Tutorial
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

# Registro de usuarios
@api.route('/signup', methods=['POST'])
def signup():
    try:
        # Recibir los datos
        data = request.get_json()
        # Obtener email, username y password del cuerpo de la solicitud
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        # Si falta email password o username, devuelve error
        if not email or not password or not username:
            print("Falta introducir email/password/username")
            return jsonify({"messsage": "Todos los campos son requeridos"}), 400
        # Verificar si existe previamente en la base de datos el email o el usuario 
        if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
            print("El usuario ya existe")
            return jsonify({"message": "El usuario ya existe"}), 400
        # Crear hash de la contraseña
        hashed_password = generate_password_hash(password)
        print("Contraseña hasheada correctamente")
        # Crear el nuevo usuario con los campos requeridos
        new_user= User(
            username=username,
            email=email,
            password=hashed_password,
            user_avatar = None,
            is_active = True
        )
        print("Intentando guardar el usuario en la base de datos...")
        # Añadir el usuario a la base de datos, y hacer el commit
        db.session.add(new_user)
        db.session.commit()
        print("Usuario guardado exitosamente")

        return jsonify({"message": "Usuario registrado exitosamente"}), 201
    # En caso de fallo, mensajes de error y revierte los cambios
    except Exception as e:
        db.session.rollback()
        print(f"Error en el endpoint /signup: {str(e)}")
        return jsonify({"message": "Error interno en el servidor", "error": str(e)}), 500
# Login usuarios
@api.route('/login', methods=['POST'])
def login():
    # Verificar si los datos están presentes
    data = request.get_json()
    # Obtener mail y contraseña del cuerpo de la solicitud
    email = data.get('email')
    password = data.get('password')
    # Validar email y contraseña
    if not email or not password:
        return jsonify({"message": "Invalid email or password"}), 400
    # Buscar en la base de datos el user filtrado por mail
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Usuario o contraseñas incorrectos"}), 401
    # Crear token de acceso usando el id
    token = create_access_token(identity=str(user.id))
    return(token)

# Obtención de usuario
@api.route('/user', methods=['GET'])
def get_user():
    try:
        # Obtener el id desde el JWT
        user_id = get_jwt_identity()
        print(f"Usuario autenticado con id: {user_id}")  

        if not user_id:
            # Si no se obtiene el id desde el JWT
            return jsonify({"message": "No se encontró el usuario autenticado en el token"}), 401

        # Buscar el usuario por id
        user = User.query.get(user_id)

        if not user:
            # Si no se encuentra el usuario en la base de datos
            print(f"Usuario con id {user_id} no encontrado en la base de datos.")
            return jsonify({"message": "Usuario no encontrado"}), 404

        # Si el usuario es encontrado, devolver la información serializada
        return jsonify(user.serialize()), 200

    except Exception as e:
        # Captura cualquier otro error y lo reporta
        print(f"Error al obtener el usuario: {str(e)}")
        return jsonify({"message": "Error al obtener el usuario", "error": str(e)}), 500

# Actualizar los datos del usuario
@api.route('/user/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    try:
        # Obtiene el user_id del usuario autenticado
        user_id = get_jwt_identity()
        # Buscar al usuario en la base de datos por el user_id
        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "Usuario no encontrado"}), 404
        # Obtener los datos enviados en el body de la solicitud
        data = request.get_json()
        # Actualizar los campos del usuario en caso de que estén
        if "email" in data:
            user.email = data["email"]
        if "username" in data:
            user.username = data["username"]
        if "user_avatar" in data:
            user.user_avatar = data["user_avatar"]
        if "password" in data:
            user.password = data["password"]
        # Commit de los cambios
        db.session.commit()

        return jsonify(user.serialize()), 200
    # En caso de error, mensaje
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"message": "Error al actualizar el usuario", "error":str(e)}), 500
    
# Eliminar un usuario
@api.route('/user/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    try:
        # Obtener el user_id del usuario autenticado
        user_id = get_jwt_identity()
        
        # Buscar al usuario con el user_id proporcionado
        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "Usuario no encontrado"}), 404
        
        # Eliminar el usuario
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "Usuario eliminado"}), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"message": "Error al eliminar el contacto"}), 500