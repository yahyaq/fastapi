import pytest
from jose import jwt
from app.config import settings
from app import schemas


def test_root(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json().get('message') == "GG world"


def test_create_user(client):
    res = client.post(
        "/users", json={"email": "test@gmail.com", "password": "pass"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "test@gmail.com"
    assert res.status_code == 201


def test_login(test_user, client):
    res = client.post(
        "/login", data={"username": test_user["email"], "password": test_user["password"]})
    login_user = schemas.Token(**res.json())
    payload = jwt.decode(login_user.access_token,
                         settings.secret_key, algorithms=settings.algorithm)
    user_id = payload.get("user_id")
    username = payload.get("username")

    assert user_id == test_user['id']
    assert username == test_user['email']
    assert login_user.token_type == "bearer"
    assert res.status_code == 200
