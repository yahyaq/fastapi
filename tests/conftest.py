from fastapi.testclient import TestClient
import pytest
from app import models
from app.oauth2 import create_access_token
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.config import settings
from app.database import get_db, Base

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():

        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user = {"email": "test@gamil.com",
            "password": "pass"}
    res = client.post("/users", json=user)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user["password"]
    return new_user


@pytest.fixture
def test_user2(client):
    user = {"email": "test123@gamil.com",
            "password": "pass"}
    res = client.post("/users", json=user)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"], "username": test_user["email"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client


@pytest.fixture
def test_posts(test_user, session, test_user2):
    post_data = [{
        "title": "1st post",
        "content": "1st content",
        "owner_id": test_user["id"]
    }, {
        "title": "2nd post",
        "content": "2nd content",
        "owner_id": test_user["id"]
    }, {
        "title": "3rd post",
        "content": "3rd content",
        "owner_id": test_user["id"]
    }, {
        "title": "3rd post",
        "content": "3rd content",
        "owner_id": test_user2["id"]
    }
    ]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, post_data)
    posts = list(post_map)

    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).all()
    return posts
