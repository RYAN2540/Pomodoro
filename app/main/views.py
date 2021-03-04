from flask import render_template,abort,redirect,url_for,request,flash,abort
from . import main
from ..models import User, Todos, Timer, Feedbacks
from .forms import LoginForm, SignUpForm, UpdateProfile
from .. import db,photos
from flask_login import login_required, current_user, login_user, logout_user
from ..email import mail_message
import datetime



@main.route('/signup', methods = ["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.username.data, password = form.password.data)
        db.session.add(user)
        db.session.commit()
        mail_message("Welcome to Pomodoro","email/welcome_user",user.email,user=user)

        return redirect(url_for('main.home'))
    title = "New Account | Pomodoro"
    return render_template('signup.html', signup_form = form, title=title)

@main.route('/', methods = ["GET", "POST"])
def home():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember.data)
            return redirect(url_for('main.todos', user_id=user.id))
        flash('Invalid username or password', 'danger')
    
    title = "Login | Pomodoro"
    return render_template('login.html', login_form = form, title=title)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.home"))

@main.route('/user/<uname>')
@login_required
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)
    
    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))



# Load todos from database
def getTodos():
	todos = Todos.query.filter_by().all()

	for todo in todos:
		if todo.completed:
			todo.completed = 'Done'
		else:
			todo.completed = 'Pending'
		todo.create_date = str(todo.create_date)
		todo.create_date = todo.create_date[0:10] 

	todos.sort(key=lambda x: x.completed, reverse=True)

	return todos


# pomodoro-tracker page
@main.route('/pomodoro', methods=["GET", "POST"])
def pomodoro():
	if request.method == 'POST':
		inputTimerTarget = request.form['pomodoroInterval']
		inputBreakTarget = request.form['breakInterval']

		# convert times to minutes:
		timerTarget = inputTimerTarget[3:]
		breakTarget = inputBreakTarget[3:]

		# save timer intervals for logged in user
		newTimer = Timer(pomodoro_interval=timerTarget, break_interval=breakTarget)
		db.session.add(newTimer)
		db.session.commit()

		todos=getTodos()
		return render_template('pomodoro.html', todos=todos, timerTarget=timerTarget, breakTarget=breakTarget,
		inputTimerTarget=inputTimerTarget, inputBreakTarget=inputBreakTarget)
	else:
		timer = Timer.query.filter_by().first()
		todos=getTodos()
		if(timer):
			inputTimerTarget = ('00:' + str(timer.pomodoro_interval))
			inputBreakTarget = ('00:' + str(timer.break_interval))
			return render_template('pomodoro.html', todos=todos, timerTarget=timer.pomodoro_interval,
			breakTarget=timer.break_interval,inputTimerTarget=inputTimerTarget,inputBreakTarget=inputBreakTarget)
		else:
			timerTarget = '25'
			breakTarget = '5'
			return render_template('pomodoro.html', todos=todos, timerTarget=timerTarget,
			breakTarget=breakTarget, inputTimerTarget=timerTarget, inputBreakTarget=breakTarget)


# todos manager
@main.route('/todos', methods=["GET", "POST"])
def todos():
	todos = getTodos()	
	return render_template('todos.html', todos = todos)


# add new todos
@main.route('/add_todo', methods=["GET", "POST"])
def add_todo():
	if request.method == 'POST':
		category = request.form['category']
		description = request.form['description']

		if category and (len(str(description).strip()) != 0):
			newTodo = Todos(category=category, 
							description=description, completed=False)
			db.session.add(newTodo)
			db.session.commit()
			todos = getTodos()
			return redirect(url_for('main.todos', todos=todos))
		else:
			flash('Please enter complete details', 'danger')
			return render_template('add_todo.html')
	else: 
		return render_template('add_todo.html')


# edit todos
@main.route('/edit_todo/<string:id>', methods=["GET", "POST"])
def edit_todo(id):
	editTodo = Todos.query.filter_by(id=id).first()
	if request.method == 'POST':
		editTodo.category = request.form['category']
		editTodo.description = request.form['description']
		if request.form['status'] == 'Done':
			editTodo.completed = True
		else:
			editTodo.completed = False
		db.session.commit()

		todos = getTodos()
		return redirect(url_for('main.todos',todos=todos))
	else:
		if editTodo and editTodo:
			return render_template('edit_todo.html',editTodo=editTodo)

# delete todos
@main.route('/delete_todo/<string:id>', methods=["POST"])
def delete_todo(id):
	delTodo = Todos.query.filter_by(id=id).first()
	db.session.delete(delTodo)
	db.session.commit()
	todos = getTodos()
	return redirect(url_for('main.todos', todos=todos))


# feedback page
@main.route('/feedback', methods=["GET", "POST"])
def feedback():	
	if request.method == 'POST':
		feedback = request.form['feedback']
		username = request.form['username']

		newFeedback = Feedbacks(username = username, feedback=feedback)
		db.session.add(newFeedback)
		db.session.commit()

		flash('Submission successful! Thank you for your feedback.', 'success')
		return render_template('feedback.html')
	else: 		
		return render_template('feedback.html')
