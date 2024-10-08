from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

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

@app.get("/users")
def read_users():
    return users_list

#Path
@app.get("/user/{id}")
def read_user(id:int):
    return search_user(id)

"""Llamar un parametro por query"""
@app.get("/userquery/")
def read_user(id: int):
      return search_user(id)

'''POST'''

@app.post("/user/")
def read_users(user: User):
    if type(search_user(user.id)) == User:
        return {"error" : "The user already exists"}
    else:                    
        users_list.append(user)



def search_user(id:int):
        users = filter(lambda user: user.id == id, users_list)
        try:
            return list(users)[0]
        except:
            return{"error": "User not found"}

