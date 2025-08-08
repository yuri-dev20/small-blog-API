import pytest

def test_create_post(client_test, sample_user):
    post = {
        "title": "Testing post",
        "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
    }
    response = client_test.post(f"/users/{sample_user.id}/posts/", json=post)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == post["title"]
    assert data["text"] == post["text"]
    assert data["owner_id"] == 1

def test_get_all_user_post(client_test, sample_user):
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
        client_test.post(f"/users/1/posts/", json=post)


    response = client_test.get(f"/users/1/posts/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


def test_fail_get_all_user_post(client_test, sample_user):
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
        client_test.post(f"/users/1/posts/", json=post)


    response = client_test.get(f"/users/99/posts/")
    assert response.status_code == 404

def test_update_post_from_user(client_test, sample_user, sample_post):
    payload = {
        "title": "Testing post",
        "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
    }

    response = client_test.put(f"/users/{sample_user.id}/posts/1", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data['title'] == "Testing post"
    assert data['text'] == "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
    assert data['owner_id'] == 1

def test_update_fails_when_user_does_not_exist(client_test, sample_user, sample_post):
    payload = {
        "title": "Testing post",
        "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
    }

    response = client_test.put(f"/users/999999/posts/1", json=payload)
    assert response.status_code == 404
    assert response.json()['detail'] == "Post não encontrado ou não pertence ao usuário"


def test_update_fails_when_post_is_not_owned_by_user(client_test, sample_user, sample_post):
    payload = {
        "title": "Testing post",
        "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
    }

    response = client_test.put(f"/users/{sample_user.id}/posts/9999999999", json=payload)
    assert response.status_code == 404
    assert response.json()['detail'] == "Post não encontrado ou não pertence ao usuário"