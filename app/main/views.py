from . import main
from ..models import Todos, Timer, Feedbacks
from flask import render_template, flash, redirect, url_for, request
from .. import db


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