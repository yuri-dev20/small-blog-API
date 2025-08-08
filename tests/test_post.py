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