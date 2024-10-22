import pytest
from app import models


@pytest.fixture
def vote_post(test_user, test_posts, session):
    new_vote = models.Vote(post_id=test_posts[3].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()


def test_vote_on_post(authorized_client, test_user, test_posts):

    res = authorized_client.post(
        "/votes", json={"post_id": test_posts[3].id, "dir": 1})

    assert res.status_code == 201


def test_vote_twice_post(authorized_client, test_user, test_posts, vote_post):

    res = authorized_client.post(
        "/votes", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 409


def test_delete_vote(authorized_client, test_user, test_posts, vote_post):

    res = authorized_client.post(
        "/votes", json={"post_id": test_posts[3].id, "dir": 0})
    assert res.status_code == 201


def test_delete_vote_non_exist(authorized_client, test_user, test_posts):

    res = authorized_client.post(
        "/votes", json={"post_id": test_posts[2].id, "dir": 0})
    assert res.status_code == 404


def test_vote_post_non_exist(authorized_client, test_posts):

    res = authorized_client.post("/votes", json={"post_id": "44", "dir": 1})
    assert res.status_code == 404


def test_vote_unauthorized_user(client, test_posts):

    res = client.post("/votes", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 401
