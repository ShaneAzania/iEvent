from app import app
from flask import flash, render_template,redirect,request,session
from app.models.user import User
from app.models.event import Event
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
# nav component import
from app.assets.repeat_page_elements import nav_render


@app.route('/new/event')
def new_event():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return redirect('/user_dash')


@app.route('/create/event/', methods = ['POST'])
def create_event():
    if 'user_id' not in session:
        return redirect ('/user_logout')
    if not Event.validate_event(reqeust.form):
        return redirect ('/new/event')
    data = {
        'name': request.form['name'],
        'lcoation': request.form ['lcoation'],
        'time': request.form ['time',]
    }
    Event.save(data)
    return redirect('/user_dash', nav_render)

