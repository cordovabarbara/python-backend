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


#Funcion para buscar un usuario en la base de datos
def search_user(username:str):
    for user in users_db:
        if user["username"] == username:
            return UserDB(**user)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not Found"
    )

#Funcion para obtener el usuario actual basado en el token
async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate":"Bearer"})
    return user

#ruta para el login
@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = search_user(form.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="The user it's not correct")

    if not form.password == user.password:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="The password is incorrect"
        )
    return {"access_token": user.username, "token_type": "bearer"}

# Ruta para obtener los datos del usuario actual
@app.get("/user/me")
async def me(user: User = Depends(current_user)):
    return user