import json
import pytest
from ToDo import app, db, Task

@pytest.fixture(scope='module')
def new_task():
    task=Task(title='Task1', description='Task 1 description', due_date='2023-03-15',status='pending') 
    return task 

@pytest.fixture(scope='module') #fixture sets the flask application configuration to testing (set in testing mode)
def test_client():
    app.config['TESTING'] = True    #check this is exist or not in testing mode 
    with app.test_client() as client:   # it will Only change in enviroment of database which will we do
        with app.app_context():   #check the set enviroment it will right or wrong
            db.create_all()       #fixture create a databse
            yield client        #Return the Test_client object means change databsed
        with app.app_context():  
            db.session.remove()     #after the work it will remove the databse 
            db.drop_all()

def test_get_all_tasks(test_client):    #(test_client = create the database connection)
    response = test_client.get('/getAll')
    assert response.status_code == 200
    assert len(response.json) == 0

def test_add_task(test_client):
    task_data = {
    'title': 'Test_Task',
    'description': 'This is a test task.',
    'due_date': '2023-03-01'
    }
    response = test_client.post('/addTask', json=task_data)
    assert response.status_code == 200
    assert response.json == {'status': 'success', 'message': 'Task added successfully'}

def test_get_all_tasks_with_one_task(test_client, new_task):
    db.session.add(new_task)
    db.session.commit()
    response = test_client.get('/getAll')
    assert response.status_code == 200
    assert len(response.json) == 2      
    assert response.json[0]['id'] == 1
    assert response.json[0]['title'] == 'Test_Task'
    assert response.json[0]['description'] == 'This is a test task.'
    assert response.json[0]['due_date'] == '2023-03-01'
    assert response.json[0]['status'] == 'pending'


def test_add_new_task_with_missing_data(test_client):
    task_data = {
    'title': 'Task1',
    # 'description': 'Missing Data Task',
    # 'due_date': '2023-03-02'
    }
    response = test_client.post('/addTask', json=task_data)

    assert response.status_code == 400
    # assert response.json['error'] == 'Bad Request'

def test_get_task_by_id(test_client):
    task = Task(title='Test Task', description='This is a test task.', due_date='2023-03-01', status='pending')
    db.session.add(task)
    db.session.commit()
    response = test_client.get(f'/getdata/{task.id}')
    assert response.status_code == 200
    assert response.json['id'] == task.id

def test_edit_task(test_client):
    task = Task(title='Test Task', description='This is a test task.', due_date='2023-03-01', status='pending')
    db.session.add(task)
    db.session.commit()
    updated_data = {
    'title': 'Updated Task Title',
    'description': 'This is an updated task description.',
    'due_date': '2023-03-02'
    }
    response = test_client.put(f'/editTask/{task.id}', json=updated_data)
    assert response.status_code == 200
    assert response.json == {'status': 'success', 'message': 'Task updated successfully'}
    updated_task = Task.query.get(task.id)
    assert updated_task.title == updated_data['title']
    assert updated_task.description == updated_data['description']   #Checking if the data coming from the database(updated_task) is equal to local data(updated_data)
    assert str(updated_task.due_date) == updated_data['due_date']

def test_mark_task_complete(test_client):
    task = Task(title='Test Task', description='This is a test task.', due_date='2023-03-01', status='Completed')
    db.session.add(task)
    db.session.commit()
    response = test_client.put(f'/markComplete/{task.id}')
    assert response.status_code == 200
    assert response.json == {'status': 'success', 'message': 'Task updated successfully'}
    updated_task = Task.query.get(task.id)
    assert updated_task.status == 'Completed'

# def test_mark_task_complete_with_invalid_id(client):
#     response = client.put('/markComplete/999')
#     assert response.status_code == 200
#     assert response.json == {'status': 'error', 'message': 'Task not found'}

def test_delete_task(test_client):
    task = Task(title='Test Task', description='This is a test task.', due_date='2023-03-01', status='pending')
    db.session.add(task)
    db.session.commit()
    response = test_client.delete(f'/deleteTask/{task.id}')
    assert response.status_code == 200
    assert response.json == {'status': 'success', 'message': 'Task deleted successfully'}
    deleted_task = Task.query.get(task.id)
    assert deleted_task is None

def test_delete_task_with_invalid_id(test_client):
    response = test_client.delete('/deleteTask/999')
    assert response.status_code == 200
    assert response.json == {'status': 'error', 'message': 'Task not found'}
