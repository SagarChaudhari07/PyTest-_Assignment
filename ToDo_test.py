import json
import pytest
from ToDo import app, db, Task

@pytest.fixture(scope='module')
def new_task():
    task=Task(title='Task1', description='Task 1 description', due_date='2023-03-15',status='pending')
    return task 

@pytest.fixture(scope='module')
def test_client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()

def test_get_all_tasks(test_client):
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
    assert response.json['error'] == 'Bad Request'

