from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    fullname: str
    email: str
    disabled: bool

class UserDB(User):
    password:str

users_db = [
    {
        "username": "barbara",
        "fullname": "Barbara Cordova",
        "email": "barbara@gmail.com",
        "disabled": False,
        "password": "123456"
    },
    {
        "username": "anais",
        "fullname": "Barbara Aliendo",
        "email": "cordova@gmail.com",
        "disabled": False,
        "password": "789456"
    }
]