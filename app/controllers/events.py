from app import app
from flask import flash, render_template,redirect,request,session
from app.models.user import User
from app.models.event import Event
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
# nav component import
from app.assets.repeat_page_elements import nav_render


@app.route('/new_event')
def new_event():
    if 'user_id' not in session:
        return redirect('/user_login')
    return render_template('event_add.html', nav = nav_render())

@app.route('/new_event_form', methods = ['POST'])
def new_event_form():
    if 'user_id' not in session:
        return redirect ('/user_login')
    if not Event.validate_event(request.form):
        return redirect ('/new_event')
    data = {
        'name': request.form['name'],
        'information': request.form['information'],
        'location': request.form['location'],
        'time': request.form['time'],
        'user_id': session['user_id']
    }
    Event.save(data)
    return redirect('/user_dash')

