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


# new_event
@app.route('/new_event')
def new_event():
    if 'user_id' not in session:
        return redirect('/user_login')
    return render_template('event_add.html', nav = nav_render())
# new_event_form
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

# event_details
@app.route('/event_details/<int:id>')
def event_details(id):
    event = Event.get_one_event({'id':id})
    print()
    print('ATTENDEE', event.attendees[0].first_name)
    print()
    return render_template('event_details.html', nav = nav_render(), event = event, attendees = event.attendees)

# event_edit
@app.route('/event_edit/<int:id>')
def event_edit(id):
    event = Event.get_one_event({'id':id})
    return render_template('event_edit.html', nav = nav_render(), event = event)
# new_event_form
@app.route('/event_edit_form', methods = ['POST'])
def event_edit_form():
    if 'user_id' not in session:
        return redirect ('/user_login')
    data = {
        'id':request.form['id']
    }
    this_event = Event.get_one_event(data)
    if session['user_id'] != this_event.user_id:
        print()
        print('UPDATE EVENT FAILED')
        print()
        return redirect (f"/event_details/{data['id']}")
    if not Event.validate_event(request.form):
        return redirect (f"/event_details/{data['id']}")
    data = {
        'id': request.form['id'],
        'name': request.form['name'],
        'information': request.form['information'],
        'location': request.form['location'],
        'time': request.form['time']
    }
    Event.update(data)
    return redirect(f'/event_details/{data["id"]}')

# event_add_attendee
@app.route('/event_add_attendee/<int:id>')
def event_add_attendee(id):
    data = {
        'id':id,
        'event_id':id,
        'user_id':session['user_id']
    }
    Event.add_attendee(data)
    event = Event.get_one_event(data)
    return redirect(f'/event_details/{id}')
# event_delete_attendee
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
    return redirect(f'/event_details/{id}')

@app.route('/event_delete/<int:id>')
def event_delete(id):
    data = {
        'id':id,
        'event_id':id,
        'user_id':session['user_id']
    }
    this_event = Event.get_one_event(data)
    if "user_id" in session:
        if session['user_id'] == this_event.user_id:
            Event.delete(data)
        return redirect(f'/user_dash')
    else:
        return redirect(f'/event_details/{id}')