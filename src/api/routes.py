"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Post, Comment, Likes, New, Tutorial
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

# Registro de usuarios
@api.route('/signup', methods=['POST'])
def handle_signup():
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
def handle_login():
    # Verificar si los datos están presentes
    data = request.json
    if not data:
        return jsonify({"message": "Se deben enviar datos formato json"}), 400
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
    return jsonify({"token": token}), 200
    
# Obtención de usuario
@api.route('/user', methods=['GET'])
@jwt_required()
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
    
# Crear un post
@api.route('/create/post', methods=['POST'])
@jwt_required()
def create_post():
    data = request.get_json()

    if not data or 'contenido' not in data:
        return jsonify({"error": "No puedes crear un post vacío"}), 400
    
    user_id = get_jwt_identity()
    new_post = Post(
        user_id = user_id,
        contenido=data['contenido'],
        post_img=data.get('post_img')
    )

    db.session.add(new_post)
    db.session.commit()

    return jsonify({"message": "Post creado con éxito"}), 201

# Eliminar post
@api.route('/delete/post/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    try:
        # Obtener al usuario autenticado y buscar el post en la base de datos por id
        user_id = get_jwt_identity()
        post = Post.query.get(post_id)
        # Si no encuentra el post o si el usuario que intenta eliminar no es el asociado al post, devuelve error
        if not post:
            return jsonify({"error": "No se ha encontrado el post"}), 404
                        #Tiene que convertirse a integer ya que lo coge como string y al compararlo devuelve error
        if post.user_id != int(user_id):
            return jsonify({"error": "No tienes permiso para eliminar este post!"}), 403
        # Borrar el post si todo es correcto, y commit en la base de datos
        db.session.delete(post)
        db.session.commit()
        # Mensaje de que todo ok
        return jsonify({"message": "Post eliminado con éxito"}), 200
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Error al eliminar el post"}), 500

# Obtener todos los posts con sus comentarios
@api.route('/feed', methods=['GET'])
@jwt_required()
def get_all_posts():
            # Obtener todos los posts ordenados por fecha
    posts = Post.query.order_by(Post.fecha_creacion.desc()).all()

    # Creo array vacío para guardar
    post_y_comm =[]
    for post in posts:
        # Agrego los datos del post y los comentarios asociados al mismo
        post_y_comm.append({
            "post": post.serialize(),
            "comments": [comment.serialize() for comment in post.comments]
        })
    # Devuelve todos los posts con sus comentarios
    return jsonify(post_y_comm), 200

# Obtener todos los posts del usuario con los comentarios
@api.route('/feed/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_posts(user_id):

    posts = Post.query.filter_by(user_id=user_id).order_by(Post.fecha_creacion.desc()).all()

    user_posts = []
    for post in posts:
        user_posts.append({
            "post": post.serialize(),
            "comments": [comment.serialize() for comment in post.comments]
        })
    
    return jsonify(user_posts), 200

# Crear comentario 
@api.route('/create/comment', methods=['POST'])
@jwt_required()
def create_comment():
    # Solicitar datos
    data = request.get_json()
    # Si falta el contenido, devuelve error
    if not data or 'contenido' not in data:
        return jsonify({"error": "No puedes crear un comentario vacío"}), 400
    #Si falta el post_id devuelve error
    if 'post_id' not in data:
        return jsonify({"error": "Falta el post_id"}), 400
    # Busca el post por id en la tabla
    post_id = data['post_id']
    post = Post.query.get(post_id)
    # Si no está, devuelve error
    if not post:
        return jsonify({"error": "El post no existe"}), 404
    # Obtiene el user id por el token
    user_id = get_jwt_identity()

    # Crea comentario con lo necesario
    new_comment = Comment(
        user_id = user_id,
        post_id = post_id,
        contenido = data['contenido'],
    )

    # Añade los cambios y hace el commit, y devuelve mensaje de éxito en la creación
    db.session.add(new_comment)
    db.session.commit()

    return jsonify({"message": "Comentario creado con éxito"}), 200

# Eliminar comentario
@api.route('/delete/comments/<int:comment_id>')
@jwt_required()
def delete_comment(comment_id):
    try:
        user_id = get_jwt_identity()
        comment = Comment.query.get(comment_id)

        if not comment:
            return jsonify({"error": "El comentario no existe"}), 404
        
        if comment.user_id != int(user_id):
            return jsonify({"error": "No tienes permiso para eliminar este comentario"}), 403
        
        db.session.delete(comment)
        db.session.commit()

    except  Exception as e:
        print(f"error: {str(e)}")
        return jsonify({"error": "Error al eliminar el comentario"}), 500