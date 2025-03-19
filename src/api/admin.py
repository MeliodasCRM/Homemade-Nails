  
import os
from flask_admin import Admin
from .models import db, User, Post, Comment, New, Tutorial, Likes
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')
    
    class userAdmin(ModelView):
        column_display_pk = True
        list_display = ("id", "name", "text")
    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(userAdmin(User, db.session))
    admin.add_view(userAdmin(Post, db.session))
    admin.add_view(userAdmin(Comment, db.session))
    admin.add_view(userAdmin(New, db.session))
    admin.add_view(userAdmin(Tutorial, db.session))
    admin.add_view(userAdmin(Likes, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))