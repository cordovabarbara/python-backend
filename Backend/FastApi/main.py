from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return "Hello World"

@app.get("/url")
def read_root():
    return {"url": "https://moure.dev/cursos/"}

"""Probando otros url, estados 200 ok, documentacion con  Swagger automaticamente"""