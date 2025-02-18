from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    username: str
    fullname: str
    email: str
    diasble: bool

users_db = {
    "mouredev":{
        "username":"brbra",
        "fullname": "Barbara Cordova",
        "email":"barbara@gmail.com",
        "diasble": False,
        "password": "123456"
    },
        "mouredev":{
        "username":"brbra2",
        "fullname": "Barbara aliendo",
        "email":"cordova@gmail.com",
        "diasble": False,
        "password": "789456"
    }
}

def search_user(username:str):
    if username in users_db:
        return users_db(users_db[username])