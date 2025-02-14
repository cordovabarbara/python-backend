from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# inicia el server: uvicorn users:app --reload 

router = APIRouter()

#Entidad User
class User(BaseModel):
    id: int
    name: str
    lastname: str
    url: str
    age: int

users_list = [User(id= 1, name = "Barbara", lastname ="Cordova", url = "https://barbara-cordova-portfolio.netlify.app/", age = 32),
              User(id= 2, name = "Anais", lastname ="Aliendo",  url = "https://barbara-cordova-portfolio.netlify.app/", age = 35),
              User(id= 3,name = "Cristobal", lastname ="Lopez", url = "https://barbara-cordova-portfolio.netlify.app/", age = 30)]

@router.get("/users")
async def read_users():
    return users_list

#Path
@router.get("/user/{id}")
async def read_user(id:int):
    return search_user(id)

"""Llamar un parametro por query"""
@router.get("/userquery/")
async def read_user(id: int):
      return search_user(id)

'''POST'''

@router.post("/user/", status_code=201)
async def read_users(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=409, detail="The user already exists")
    users_list.append(user)
    return{ "message":"User created successfully", "user": user}
    

'''PUT'''
@router.put("/user/")
async def read_users(user: User):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    if not found:
        return {"error" : "failed to update user"}
    else:
        return user
    

    '''Delete'''
@router.delete("/user/{id}")
async def read_user(id:int):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
            return {"The user has been successfully deleted"}
    if not found:
        return {"error": "Error deleting user"}



def search_user(id:int):
        users = filter(lambda user: user.id == id, users_list)
        try:
            return list(users)[0]
        except:
            return{"error": "User not found"}

