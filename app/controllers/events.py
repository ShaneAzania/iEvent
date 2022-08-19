from app import app
from flask import flash, render_template,redirect,request,session
from app.models.user import User
from app.models.event import Event
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import datetime
todays_date = datetime.datetime.now()
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

@app.route('/event_details/<int:id>')
def event_details(id):
    event = Event.get_one_event({'id':id})
    return render_template('event_details.html', nav = nav_render(), event = event, attendees = event.attendees)

@app.route('/event_add_attendee/<int:id>')
def event_add_attendee(id):
    data = {
        'id':id,
        'event_id':id,
        'user_id':session['user_id']
    }
    Event.add_attendee(data)
    event = Event.get_one_event(data)
    return render_template('event_details.html', nav = nav_render(), event = event, attendees = event.attendees)
@app.route('/event_delete_attendee/<int:id>')
def event_delete_attendee(id):
    if 'user_id' not in session:
        return redirect(f'/event_details/{id}')
    data = {
        'id':id,
        'event_id':id,
        'user_id':session['user_id']
    }
    Event.delete_attendee(data)
    event = Event.get_one_event(data)
    return render_template('event_details.html', nav = nav_render(), event = event, attendees = event.attendees)

