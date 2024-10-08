from fastapi import Response, HTTPException, status, Depends, APIRouter
from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model=List[schemas.PostOut])
def gg(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
       limit: Optional[int] = None, skip: int = 0, search: Optional[str] = ''):
    # cursor.execute("""SELECT * FROM posts """)
    # post = cursor.fetchall()
    # print(post)
    print(search)

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("likes")).outerjoin(
        models.Vote, models.Vote.post_id == models.Post.id).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # print(results)

    return posts


@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=schemas.Posts)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" INSERT INTO posts (title, content, publish) VALUES (%s, %s, %s) RETURNING *""",
    #                (post.title, post.content, post.publish))

    # new_post = cursor.fetchone()
    # conn.commit()
    print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("likes")).outerjoin(
        models.Vote, models.Vote.post_id == models.Post.id).group_by(models.Post.id).filter(models.Post.id == id).first()
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found GG")
    #     response.status_code = status.HTTP_404_NOT_FOUND
    return post


@ router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute(
    #     """ DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist GG")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform the requested action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@ router.put("/{id}", response_model=schemas.Posts)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, publish = %s WHERE id = %s RETURNING * """,
    #                (post.title, post.content, post.publish, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    # index = find_index_post(id)

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_update = post_query.first()
    if post_update == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist GG")
    if post_update.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform the requested action")
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    # post_dump = post.model_dump()
    # print(post_dump)
    # post_dump["id"] = id
    # print(post_dump)
    # my_posts[index] = post_dump
    return post_query.first()
