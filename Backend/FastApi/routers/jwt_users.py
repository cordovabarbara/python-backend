from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta

app = FastAPI()

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1



oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

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

# Hashear las contraseñas antes de usarlas
for user in users_db:
    user["password"] = crypt.hash(user["password"])

#Funcion para buscar un usuario en la base de datos
def search_user(username:str):
    for user in users_db:
        if user["username"] == username:
            return UserDB(**user)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not Found"
    )


@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = search_user(form.username)
    
    if not user or not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    access_token = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }

    return {"access_token": access_token, "token_type": "bearer"}