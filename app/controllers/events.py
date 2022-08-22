from hashlib import new
from sqlite3 import Date
from posixpath import split
from app import app
from flask import flash, render_template,redirect,request,session
from app.models import message
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
        #add attendee limit 
        'user_id': session['user_id']
    }
    Event.save(data)
    return redirect('/user_dash')

# event_details
@app.route('/event_details/<int:id>')
def event_details(id):
    # collect event object
    event = Event.get_one_event({'id':id})
    # format location string for html link
    new_location_string = ''
    for element in event.location.split(','):
        new_element = ''
        for char in element:
            if char == ' ':
                new_element += '%20'
            if char == '#':
                new_element += 'Apt '
            else:
                new_element += char
        new_location_string += new_element
    # collect messages
    messages = message.Message.get_all_messages_for_event({"event_id":id})
    # print()
    # print('MESSAGES', messages[0])

    return render_template(
        'event_details.html', nav = nav_render(), 
        attendees = event.attendees, 
        event = event, 
        messages = messages, 
        location = new_location_string
    )

# event_edit
@app.route('/event_edit/<int:id>')
def event_edit(id):
    event = Event.get_one_event({'id':id})
    return render_template('event_edit.html', nav = nav_render(), event = event)
# event_edit_form
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
# event_delete
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


@app.route('/event_search')
def event_search():
    if 'user_id' in session:
        events_all = Event.get_all_events()
        return render_template('event_search.html', nav = nav_render(), events_all = events_all)
    else:
        return redirect('/user_login')


#hf just added to main 
@app.route('/event_search_form', methods = ['POST'])
def event_search_form():
    if 'user_id' in session:
        search_term = request.form['search']
        search_word_array = search_term.split(' ')
        # get events list
        events_all = Event.get_all_events()
        search_results = []
        # check each event.name to see if the search words are in the name
        for event in events_all:
            valid = True
            # filter from form to be accessed from event object
            filter_form = request.form['filter']
            # event object field to be accessed
            event_field = {
                'name': event.name,
                'location': event.location,
                'time': event.time,
                'user_id': event.user.first_name + ' ' + event.user.last_name,
            }
            # check if each word is in search_term
            for word in search_word_array:
                # check if filter type is date/time
                if type(event_field[filter_form]) == type(todays_date):
                    event_date = event_field[filter_form].strftime('%Y-%m-%d')
                    print('DATE Of Event:', event_date)
                    print('DATE Of Search:', search_term)
                    print()
                    if event_date != search_term:
                        valid = False
                # if filter type isn't date/time
                elif word.lower() not in event_field[filter_form].lower():
                    valid = False
            if valid:
                search_results.append(event)
        if type(event_field[filter_form]) == type(todays_date):
            search_term = ''
        print('search_results'.upper(),search_results)

        return render_template(
            'event_search.html', 
            nav = nav_render(), 
            events_all = search_results, 
            filter_ = request.form['filter'], 
            search_term = search_term
        )
    else:
        return redirect('/user_login')

