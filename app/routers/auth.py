from fastapi import APIRouter, HTTPException, Response, status, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database
from .. import schemas, models, utils, oauth2

router = APIRouter(
    tags=['Login']
)


@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials")

    # user_credentials.password = utils.hash(user_credentials.password)

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    access_token = oauth2.create_access_token(
        data={"user_id": user.id, "username": user_credentials.username})

    return {"access_token": access_token, "token_type": "bearer"}
