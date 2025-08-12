from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import Session

from app.schemas.token import Token
from app.auth.service import auth_user
from app.database.db import get_db
from app.auth.security import ACCESS_TOKEN_EXPIRE, create_access_token

router = APIRouter(prefix='/login')

@router.post('/')
def login_for_access_token(db: Annotated[Session, Depends(get_db)], form_data: Annotated[OAuth2PasswordRequestForm, Depends()],) -> Token:
    user = auth_user(db, form_data.username, form_data.password) # form_data.username no caso do meu projeto recebe um email

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE)
    access_token = create_access_token(data={'sub': user.email}, expire_delta=access_token_expires)

    return Token(access_token=access_token, token_type='Bearer')