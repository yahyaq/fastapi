import pytest
from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts")

    def validate_post(post):
        return schemas.PostOut(**post)

    post_map = map(validate_post, res.json())
    post = list(post_map)
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


def test_unauthorized_get_all_posts(client, test_posts):
    res = client.get("/posts")
    assert res.json().get("detail") == "Not authenticated"
    assert res.status_code == 401


def test_unauthorized_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get("/posts/88888")
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content


@pytest.mark.parametrize("title, content, publish", [
    ("1st GG", "Good GG", True),
    ("2nd GG", "Nice GG", False),
    ("3rd GG", "Awesome GG", True)
])
def test_create_post(authorized_client, test_user, test_posts, title, content, publish):
    res = authorized_client.post(
        "/posts", json={"title": title, "content": content, "publish": publish})
    print(res.json())
    create_post = schemas.Posts(**res.json())
    assert res.status_code == 201
    assert create_post.title == title
    assert create_post.content == content
    assert create_post.publish == publish
    assert create_post.owner_id == test_user['id']


def test_create_post_default_publish_true(authorized_client, test_user, test_posts):
    res = authorized_client.post(
        "/posts", json={"title": "GG", "content": "GG too"})
    post_creat = schemas.Posts(**res.json())
    assert res.status_code == 201
    assert post_creat.publish == True


def test_unauthorized_user_create_post(client, test_user, test_posts):
    res = client.post("/posts", json={"title": "GG", "content": "GG too"})
    assert res.status_code == 401


def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    response = authorized_client.get("/posts")
    assert res.status_code == 204
    assert len(response.json()) == len(test_posts) - 1


def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete("/posts/44")
    assert res.status_code == 404


def test_delete_other_user_posts(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403


def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "Updated GG",
        "content": "new content",
        "publish": False,
        "id": test_posts[0].id
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    update_post = schemas.PostCreate(**res.json())
    assert res.status_code == 200
    assert update_post.title == data["title"]
    assert update_post.content == data["content"]
    assert update_post.publish == data["publish"]


def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):

    data = {
        "title": "Updated GG",
        "content": "new content",
        "publish": False,
        "id": test_posts[3].id
    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403


def test_unauthorized_user_update_post(client, test_user, test_posts):

    data = {
        "title": "Updated GG",
        "content": "new content",
        "publish": False,
        "id": test_posts[3].id
    }
    res = client.put(f"/posts/{test_posts[0].id}", json=data)
    assert res.status_code == 401


def test_updata_non_exist_post(authorized_client, test_user, test_posts):
    data = {
        "title": "Updated GG",
        "content": "new content",
        "publish": False,
        "id": test_posts[3].id
    }
    res = authorized_client.put("/posts/44", json=data)
    assert res.status_code == 404
