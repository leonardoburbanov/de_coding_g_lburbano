import json
from app import create_app
import pytest
import os

input_dir = './test/input'

@pytest.fixture
def app():
    app = create_app()
    yield app

def test_test_endpoint(app):
    response = app.test_client().get('/test')
    assert response.status_code == 200
    assert json.loads(response.data.decode('utf-8'))== {"test": "OK"}

def test_upload_csv_departments_endpoint(app):
    file = 'departments.csv'
    file_path = os.path.join(input_dir, file)
    with open(file_path, 'rb') as f:
            response = app.test_client().post('/upload_csv?table=departments&batch_size=10', data={'file': f})
    assert response.status_code == 200

def test_upload_csv_jobs_endpoint(app):
    file = 'jobs.csv'
    file_path = os.path.join(input_dir, file)
    with open(file_path, 'rb') as f:
            response = app.test_client().post('/upload_csv?table=jobs&batch_size=10', data={'file': f})
    assert response.status_code == 200


def test_upload_csv_employees_endpoint(app):
    file = 'hired_employees.csv'
    file_path = os.path.join(input_dir, file)
    with open(file_path, 'rb') as f:
            response = app.test_client().post('/upload_csv?table=employees&batch_size=10', data={'file': f})
    assert response.status_code == 200


def test_upload_csv_employees_with_batch_size_1200_endpoint(app):
    file = 'hired_employees.csv'
    file_path = os.path.join(input_dir, file)
    with open(file_path, 'rb') as f:
            response = app.test_client().post('/upload_csv?table=employees&batch_size=1200', data={'file': f})
    assert response.status_code == 200
