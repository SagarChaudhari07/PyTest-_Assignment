from flask import Flask, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Root@localhost:3306/todoApp'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    description = db.Column(db.String(200))
    due_date = db.Column(db.Date)
    status = db.Column(db.String(10))

    def __init__(self, title, description, due_date, status):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.status = status

@app.route('/getAll')
def get():
    tasks = Task.query.all()
    result = []
    for task in tasks:
        task_data = {}
        task_data['id'] = task.id
        task_data['title'] = task.title
        task_data['description'] = task.description
        task_data['due_date'] = str(task.due_date)
        task_data['status'] = task.status
        result.append(task_data)
    return result

@app.route("/addTask", methods = ['post'])
def saveTask():
    title = request.json['title']
    description = request.json['description']
    due_date = request.json['due_date']
    status = "pending"
    task = Task(title, description, due_date, status)
    db.session.add(task)
    db.session.commit()
    return {'status': 'success', 'message': 'Task added successfully'}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


#     {
#     "title" : "  PROCESS",
#     "description" : " completed of my sql database ",
#     "due_date" : "25-2-23"
# }