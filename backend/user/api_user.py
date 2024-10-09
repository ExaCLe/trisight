import os
from datetime import datetime, timedelta, timezone
from sqlite3 import IntegrityError
from typing import Annotated
import uuid

import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import smtplib
from email.mime.text import MIMEText

from backend.utils import get_db
from backend.schemas import (
    ForgetPassword,
    ResetPassword,
    Token,
    TokenData,
    UserToRegister,
    UserResponse,
)
from backend import models

router = APIRouter()

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db: Session, email: str) -> models.User:
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: Session, username: str) -> models.User:
    return db.query(models.User).filter(models.User.username == username).first()


def authenticate_user(db: Session, email: str, password: str):
    user = get_user(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(db: Session, data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    issued_at = datetime.now(timezone.utc)
    to_encode.update({"exp": expire, "iat": issued_at.timestamp()})
    encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=ALGORITHM)

    try:
        user = get_user_by_username(db, data["sub"])
        user.issued_at = issued_at
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=422, detail=f"Constraint error: {e.orig}")

    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        issued_at: datetime = payload.get("iat")
        issued_at = datetime.fromtimestamp(issued_at, tz=timezone.utc)
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception

    if (
        issued_at is not None
        and user.issued_at is not None
        and issued_at.replace(tzinfo=None) < user.issued_at
    ):
        raise credentials_exception
    return user


@router.post("/login")
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(db, data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserResponse)
def read_users_me(
    current_user: Annotated[models.User, Depends(get_current_user)],
):
    return current_user


@router.post("/register", response_model=UserResponse)
def register_user(user: UserToRegister, db: Session = Depends(get_db)) -> UserResponse:
    # check that the user does not already exist
    if get_user_by_username(db, user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )

    # check that the email is not already registered
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # hash the password and insert into the database otherwise
    user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password),
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=422, detail=f"Constraint error: {e.orig}")

    db.refresh(user)

    return UserResponse(
        id=user.id,
        created=user.created,
        username=user.username,
        email=user.email,
    )


@router.get("/exists/{username}")
def check_user_exists(username: str, db: Session = Depends(get_db)):
    user = get_user_by_username(db, username)
    return {"exists": user is not None}


@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    current_user = await get_current_user(token, db)

    try:
        current_user.issued_at = datetime.now(timezone.utc)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=422, detail=f"Constraint error: {e.orig}")

    return {"detail": "Successfully logged out"}


def create_password_reset_token(db: Session, user_id: str):
    token = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(hours=1)  # Token expires in 1 hour

    reset_token = models.PasswordResetToken(
        user_id=user_id, token=token, expires_at=expires_at
    )
    db.add(reset_token)
    db.commit()

    return token


def send_password_reset_email(email: str, token: str):
    reset_url = f"{os.getenv('FRONTEND_URL')}/reset-password?token={token}"
    msg = MIMEText(f"Click the following link to reset your password: {reset_url}")

    msg["Subject"] = "Reset Your Password"
    msg["From"] = f"no-reply@{os.getenv('FRONTEND_URL')}"
    msg["To"] = email

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("trisight.game@gmail.com", os.getenv("EMAIL_PASSWORD"))
        server.send_message(msg)


@router.post("/forgot-password")
def forgot_password(data: ForgetPassword, db: Session = Depends(get_db)):
    user = get_user(db, data.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = create_password_reset_token(db, user.id)
    send_password_reset_email(data.email, token)

    return {"msg": "Password reset email sent"}


@router.post("/reset-password")
def reset_password(data: ResetPassword, db: Session = Depends(get_db)):
    reset_token = (
        db.query(models.PasswordResetToken)
        .filter(models.PasswordResetToken.token == data.token)
        .first()
    )

    if not reset_token or reset_token.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = db.query(models.User).filter(models.User.id == reset_token.user_id).first()
    user.hashed_password = get_password_hash(data.new_password)

    db.delete(reset_token)
    db.commit()

    return {"msg": "Password has been reset"}
