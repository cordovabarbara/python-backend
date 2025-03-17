from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from jwt.exceptions import InvalidTokenError

router = APIRouter()

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1
SECRET_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJiYXJiYXJhIiwiZXhwIjoxNzQwNTI5Nzg3fQ.GXbbH2WdlS-uF9PIUGHE30OYh1Vo4M3vN9sCd-JUGwg"

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username: str
    fullname: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

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

# Función para buscar un usuario en la base de datos
def search_user(username: str):
    for user in users_db:
        if user["username"] == username:
            return UserDB(**user)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not Found"
    )

async def auth_user(token: str = Depends(oauth2)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"}
            )
        return search_user(username)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )

# Función para obtener el usuario actual basado en el token
async def current_user(user: UserDB = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive User"
        )
    return user

@router.post("/login")
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

    # Codificar el token y convertirlo a cadena
    token = jwt.encode(access_token, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

# Ruta para obtener los datos del usuario actual
@router.get("/user/me")
async def me(user: UserDB = Depends(current_user)):
    return User(**user.dict())