from hashlib import new
from posixpath import split
from app import app
from flask import flash, render_template,redirect,request,session
from app.models.message import Message
# nav component import
from app.assets.repeat_page_elements import nav_render


# message_create_form
@app.route('/message_create_form', methods  = ['POST'])
def message_create_form():
    if 'user_id' not in session:
        return redirect('/user_login')
    data = {
        'message': request.form['message'],
        'user_id': session['user_id'],
        'event_id': request.form['event_id']
    }
    if not Message.validate(data):
        return redirect(f'event_details/{data["event_id"]}')
    Message.create(data)
    return redirect(f'event_details/{data["event_id"]}')

# message_delete
@app.route('/message_delete/<int:message_id>/<int:event_id>')
def message_delete(message_id,event_id):
    if 'user_id' not in session:
        return redirect('/user_login')
    # if current user not message owner, then redirect
    data = {
        'id': message_id
    }
    message = Message.get_one_message(data)
    if session['user_id'] != message.user_id:
        return redirect(f'/event_details/{event_id}')
    # delete message if condisions pass
    Message.delete(data)
    return redirect(f'/event_details/{event_id}')