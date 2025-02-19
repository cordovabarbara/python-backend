from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

#un estandar para trabajar la autenticacion
oauth2 = OAuth2PasswordBearer(tokenUrl="login")


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

async def current_user(token:str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="the password is not correct")


@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not users_db:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="The user it's not correct")

    user = search_user(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The password is incorrect")
    return {"access_token": user.username, "token_type": "bearer"}

@app.get("/user/me")
async def me(user: User = Depends(current_user)):
    return user