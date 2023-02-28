import json
import pytest
from ToDo import app, db, Task

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
    'title': 'Test Task',
    'description': 'This is a test task.',
    'due_date': '2023-03-01'
    }
    response = test_client.post('/addTask', json=task_data)
    assert response.status_code == 200
    assert response.json == {'status': 'success', 'message': 'Task added successfully'}


