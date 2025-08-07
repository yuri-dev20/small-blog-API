import pytest
from app.models.user import User

def test_create_user(client_test):
    user_data = {
        'name':"Maria Die",
        'email':"mariadie@gmail.com",
        'password':"coxinha456",
        'admin':0,
        'user_active':1
    }

    # Enviado o post com json
    response = client_test.post('/users/', json=user_data)

    assert response.status_code == 200
    data = response.json()
    assert data['name'] == user_data["name"]
    assert data['email'] == user_data["email"]
    assert 'id' in data
    assert 'password' not in data # POR MOTIVOS OBVIOS isso não pode estar aqui

def test_create_user_with_existing_email(client_test, sample_user):
    user_data = {
        'name':"Sam Deo",
        'email':"jhondoe@gmail.com",
        'password':"coxinha789",
        'admin':0,
        'user_active':1
    }

    response = client_test.post('/users/', json=user_data)

    assert response.status_code == 409
    assert 'Email já cadastrado' in response.json()['detail']

def test_read_users(client_test, sample_user):
    user_data = {
        'name':"Maria Die",
        'email':"mariadie@gmail.com",
        'password':"coxinha456",
        'admin':0,
        'user_active':1
    }

    client_test.post('/users/', json=user_data)
    response = client_test.get('/users/')

    assert response.status_code == 200
    data = response.json()
    assert 'password' not in data[0]
    assert len(data) == 2

def test_read_users_with_query_parameter(client_test, sample_user):
    user_data = {
        'name':"Maria Die",
        'email':"mariadie@gmail.com",
        'password':"coxinha456",
        'admin':0,
        'user_active':1
    }

    client_test.post('/users/', json=user_data)
    response = client_test.get('/users/?limit=1')

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1


def test_read_user(client_test, sample_user):
    user_data = {
        'name':"Maria Die",
        'email':"mariadie@gmail.com",
        'password':"coxinha456",
        'admin':0,
        'user_active':1
    }

    client_test.post('/users/', json=user_data)
    response = client_test.get('/users/1')

    assert response.status_code == 200
    data = response.json()
    assert 'password' not in data
    assert data['name'] == 'Jhon Doe'
    assert data['email'] == 'jhondoe@gmail.com'
