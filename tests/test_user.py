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
