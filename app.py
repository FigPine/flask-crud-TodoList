# Flask CRUD app based on Jake Rieger's Flask tutorial:
# https://youtu.be/Z1RJmh_OqeA?si=tovkiN4RtfibB7K6


from flask import Flask, render_template,request,redirect # importing Flask from the flask module
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__) # creating an instance of the Flask class
#__name__ is a special Python variable that tells Flask where to look for resources like templates and static files
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' #tells the app where the database is located
# /// for relative path and //// for absolute path
db = SQLAlchemy(app) #database will be initialized with the Flask app instance, ie, with the settings defined in the app.config

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

def __repr__(self): 
    return f'<Task {self.id!r}>' # returns task and the id of the task


@app.route('/', methods=['POST','GET']) # defining a route for the root URL
def index(): #defining the function that will be called when the root URL is accessed
    if request.method == 'POST':
        task_content = request.form['content'] # getting the content of the task from the form, content is the id of the input field in the HTML form, its in index.html in name
        new_task = Todo(content=task_content) #create a todo object that can tap into its contents 

        try:                           #push it to a database
            db.session.add(new_task) #adding the new task to the database session
            db.session.commit() #committing the session to save the changes to the database
            return redirect('/') #redirecting to the root URL after adding the task
        except:
            return 'There was an issue adding your task.'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()  # if the request method is GET, we retrieve all tasks from the database, ordered by date created, newest to oldest
        return render_template('index.html', tasks=tasks) #rendering the index.html template and passing the tasks to it

@app.route('/delete/<int:id>') # defining a route to delete a task, <int:id> captures the id of the task to be deleted   
def delete(id):
    task_to_delete = Todo.query.get_or_404(id) # retrieving the task to be deleted from the database, if not found, it raises a 404
    try:
        db.session.delete(task_to_delete) # deleting the task from the database session
        db.session.commit() # committing the session to save the changes
        return redirect('/') # redirecting to the root URL after deletion
    except:
        return 'There was a problem deleting the task'
    
@app.route('/update/<int:id>', methods=['GET','POST']) # defining a route to update a task, <int:id> captures the id of the task to be updated
def update(id):
    task = Todo.query.get_or_404(id) # retrieving the task to be updated from the database, if not found, it raises a 404

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updateing your task.'
        
    else:
        return render_template('update.html', task=task) # rendering the update.html template and passing the task to it

if __name__ == "__main__": # checking if this script is being run directly
    app.run(debug=True) # running the Flask application with debug mode enabled 
