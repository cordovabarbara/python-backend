from fastapi import FastAPI
from routers import products, users


app = FastAPI()

#Routers
app.include_router(products.router)
app.include_router(users.router)

@app.get("/")
async def read_root():
    return "Hello World"

@app.get("/url")
async def read_root():
    return {"url": "https://moure.dev/cursos/"}

"""Probando otros url, estados 200 ok, documentacion con  Swagger automaticamente"""