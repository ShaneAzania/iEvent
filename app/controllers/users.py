from app import app
from flask import flash, render_template,redirect,request,session
from app.models.user import User
from app.models import event
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import datetime
todays_date = datetime.datetime.now()
# nav component import
from app.assets.repeat_page_elements import nav_render

#Home
@app.route('/')
def index():
    return redirect('/user_login')

#join
@app.route('/user_join')
def join(): 
    if 'user_id' in session:
        return redirect('/')
    else:
        return render_template('user_join.html', nav = nav_render())







@app.route('/user_join_form', methods = ['POST'])
def user_register_form():
    if User.validate_form(request.form):
        data = {
            'first_name' : request.form['first_name'],
            'last_name' : request.form['last_name'],
            'email' : request.form['email'],
            'password' : bcrypt.generate_password_hash(request.form['password'])
        }
        #  is email address already registered to existing account
        if User.get_by_email({'email': data['email']}):
            flash('Email alread registered to existing user. Please use another email address.')
            print('======UNSUCCESSFUL DATABASE INSERT')
            session['first_name'] = request.form['first_name']
            session['last_name'] = request.form['last_name']
            session['email'] = request.form['email']
            return redirect('/user_join')

        #create user and set current user in session
        user = User.get_one({'id':User.create(data)})
        session.clear()
        session['user_id'] = user.id
        session['first_name'] = user.first_name
        session['last_name'] = user.last_name
        session['email'] = user.email
        return redirect('/')
    else:
        print('======UNSUCCESSFUL DATABASE INSERT')
        session['first_name'] = request.form['first_name']
        session['last_name'] = request.form['last_name']
        session['email'] = request.form['email']
        return redirect('/user_join')


# login
@app.route('/user_login')
def user_login():
    if 'user_id' in session:
        return redirect('/user_dash')
    return render_template('user_login.html', nav = nav_render())




#edit user #####################################
@app.route('/user_details/<int:id>')
def edit_user(user_id):
    if 'user_id' not in session:
        return redirect ('/logout')
    user_data = {
        "id": session[user_id]
    }
    return render_template("user_details.html", user=User.get_one(user_id))




@app.route('/user_login_form', methods = ['POST'])
def user_login_form():
    # Validate User Login
    if User.validate_form(request.form):
        # check if user exists
        user = User.get_by_email({'email': request.form['email']})
        if user:
            # Check if password matches
            if bcrypt.check_password_hash(user.password, request.form['password']):
                # login
                session.clear()
                session['user_id'] = user.id
                session['first_name'] = user.first_name
                session['last_name'] = user.last_name
                session['email'] = user.email
                return redirect('/user_dash')
            else:
                # go back to login page
                session['email'] = request.form['email']
                session['password'] = request.form['password']
                flash('Invalid Password')
                return redirect('/user_login')
        else:
            flash('Invalid user')
            return redirect('/user_login')
    else:
        # if validation failed, send back to login page
        return redirect('/user_login')
#log out
@app.route('/user_logout')
def user_logout():
    session.clear()
    return redirect('/user_login')

#dash
@app.route('/user_dash')
def user_dash():
    if 'user_id' in session:
        events_past = event.Event.get_all_events_past()
        # events_all = event.Event.get_all_events()
        events_today = []
        events_future = event.Event.get_all_events_future()
        for e in events_future:
            if e.time.strftime('%m/%d/%Y') == todays_date.strftime('%m/%d/%Y'):
                events_today.append(e)
        return render_template('user_dash.html', nav = nav_render(), events_future = events_future, events_today = events_today, events_past = events_past, todays_date = todays_date)
    else:
        return redirect('/user_login')