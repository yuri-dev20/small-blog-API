import pytest
import jwt

from app.auth.security import SECRET_KEY, ALGORITHM, create_access_token

def test_login_success(client_test, sample_user):
    response = client_test.post('/login/', data={"username": "jhondoe@gmail.com", "password": "coxinha123"})

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "Bearer"

    # Decodificação do JWT
    payload = jwt.decode(data["access_token"], SECRET_KEY, algorithms=[ALGORITHM])
    assert payload.get('sub') =="jhondoe@gmail.com"

def test_create_post_auth_success(client_test, sample_user):
    token = create_access_token(data={"sub": sample_user.email})
    headers = {"Authorization": f"Bearer {token}"}

    post_data = {
        "title": "Test title",
        "text": "Test text",
    }

    response = client_test.post('/users/me/posts/', json=post_data, headers=headers)

    assert response.status_code == 200
    data = response.json()

    assert data["title"] == post_data["title"]
    assert data["text"] == post_data["text"]
    assert data["owner_id"] == 1

def test_create_post_auth_failed(client_test, sample_user):
    post_data = {
        "title": "Test title failed",
        "text": "Test without authorization",
    }

    response = client_test.post('/users/me/posts/', json=post_data)

    # Vem do get_current_user
    assert response.status_code == 401

def test_get_all_user_posts_with_auth(client_test, sample_user):
    token = create_access_token(data={"sub": sample_user.email})
    headers = {"Authorization": f"Bearer {token}"}

    posts = [
        {
        "title": "Testing post 1",
        "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        },
        {
        "title": "Testing post 2",
        "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        },
        {
        "title": "Testing post 3",
        "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        }
    ]

    for post in posts:
        client_test.post(f"/users/me/posts/", json=post, headers=headers)


    response = client_test.get(f"/users/me/posts/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


def test_fail_get_all_user_posts_with_auth(client_test, sample_user):
    token = create_access_token(data={"sub": sample_user.email})
    headers = {"Authorization": f"Bearer {token}"}
    posts = [
        {
        "title": "Testing post 1",
        "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        },
        {
        "title": "Testing post 2",
        "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        },
        {
        "title": "Testing post 3",
        "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        }
    ]

    for post in posts:
        client_test.post(f"/users/me/posts/", json=post, headers=headers)


    response = client_test.get(f"/users/me/posts/")
    assert response.status_code == 401

def test_success_get_single_post_from_user_with_auth(client_test, sample_user, sample_post):
    token = create_access_token(data={"sub": sample_user.email})
    headers = {"Authorization": f"Bearer {token}"}

    response = client_test.get(f"/users/me/posts/1", headers=headers)
    assert response.status_code == 200

def test_failed_get_single_post_from_user_with_auth(client_test, sample_user, sample_post):
    response = client_test.get(f"/users/me/posts/1")
    assert response.status_code == 401


def test_update_post_from_user_with_auth(client_test, sample_user, sample_post):
    token = create_access_token({"sub": sample_user.email})
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "title": "Testing post",
        "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
    }

    response = client_test.put(f"/users/me/posts/1", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data['title'] == "Testing post"
    assert data['text'] == "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
    assert data['owner_id'] == 1

def test_update_fails_without_auth(client_test, sample_user, sample_post):
    payload = {
        "title": "Testing post",
        "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
    }

    response = client_test.put(f"/users/me/posts/1", json=payload)
    assert response.status_code == 401
    assert response.json()['detail'] == 'Not authenticated'


def test_update_fails_when_post_is_not_owned_by_user_with_auth(client_test, sample_user, sample_post):
    token = create_access_token({"sub": sample_user.email})
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "title": "Testing post",
        "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
    }

    response = client_test.put(f"/users/me/posts/9999999999", json=payload, headers=headers)
    assert response.status_code == 404
    assert response.json()['detail'] == "Post não encontrado ou não pertence ao usuário"

def test_deleting_a_post_with_auth(client_test, sample_user, sample_post):
    token = create_access_token({"sub": sample_user.email})
    headers = {"Authorization": f"Bearer {token}"}
    delete_response = client_test.delete(f"/users/me/posts/1", headers=headers)
    get_response = client_test.get(f"/users/me/posts/1", headers=headers)
    
    assert get_response.status_code == 404
    assert delete_response.status_code == 200
    data = delete_response.json()
    assert data['title'] == "Testing post"
    assert data['text'] == "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
    assert data['owner_id'] == 1