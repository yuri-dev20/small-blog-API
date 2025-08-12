import pytest
import jwt

from app.auth.security import SECRET_KEY, ALGORITHM

def test_login_success(client_test, sample_user):
    response = client_test.post('/login/', data={"username": "jhondoe@gmail.com", "password": "coxinha123"})

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "Bearer"

    # Decodificação do JWT
    payload = jwt.decode(data["access_token"], SECRET_KEY, algorithms=[ALGORITHM])
    assert payload.get('sub') =="jhondoe@gmail.com"