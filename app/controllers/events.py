from app import app
from flask import flash, render_template,redirect,request,session
from app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
# nav component import
from app.assets.repeat_page_elements import nav_render

@app.route('/new/event')
def new_event():
    if 'user_id' not in session:
        return redirect('/user_logout')
   data = {"id":session['user_id']
    }
    return render_template('user_add_event.html',user=User.get_by_id(data), nav = nav_render())  