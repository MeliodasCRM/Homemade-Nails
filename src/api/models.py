from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    user_avatar = db.Column(db.String(255))
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "img": self.user_avatar,
            # do not serialize the password, its a security breach
        }

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    post_img = db.Column(db.String(255))
    fecha_creacion = db.Column(db.DateTime(), default=func.now())
    # Relaciones
    user = db.relationship('User', backref='posts', lazy=True)

    def serialize(self):
        return{
            "id": self.id,
            "user_id": self.user_id,
            "contenido": self.contenido,
            "post_img": self.post_img,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    fecha_comentario = db.Column(db.DateTime(), default=func.now())
    # Relaciones
    post = db.relationship('Post', backref='comments', lazy=True)
    user = db.relationship('User', backref='comments', lazy=True)

    def serialize(self):
        return{
            "id":self.id,
            "post_id":self.post_id,
            "user_id":self.user_id,
            "contenido":self.contenido,
            "fecha_comentario":self.fecha_comentario.isoformat() if self.fecha_comentario else None
        }
class New(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    imagen_url= db.Column(db.String(255), nullable=False)
    fecha_publicacion= db.Column(db.DateTime)

    def serialize(self):
        return{
            "id": self.id,
            "titulo":self.titulo,
            "imagen_url":self.imagen_url,
            "fecha_publicacion":self.fecha_publicacion.isoformat() if self.fecha_publicacion else None
        }
class Tutorial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    titulo= db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    video_url = db.Column(db.String, nullable=False)
    fecha_creacion=db.Column(db.DateTime, default=func.now(), nullable=False)
    # Relaciones
    user = db.relationship('User', backref='tutorials', lazy=True)

    def serialize(self):
        return{
            "id":self.id,
            "user_id":self.user_id,
            "titulo":self.titulo,
            "descripcion":self.descripcion,
            "video_url":self.video_url,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }
class Likes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    # Relaciones
    user = db.relationship('User', backref='likes', lazy=True)
    post = db.relationship('Post', backref='likes', lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "post_id": self.post_id,
        }