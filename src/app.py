#Kör din FASTAPI-applikation: fastapi dev src/app.py
#Om du vill återkomma till miljön senare och starta virtuella miljö: myenv\Scripts\Activate.ps1
#Avaktivera miljön: deactivate


# -*- coding: utf-8 -*-
#FastAPI is a modern, fast (high-performance), web framework for building APIs with Python based on standard Python type hints.
from fastapi import FastAPI, Header


app = FastAPI()

#path is / and operation is GET
@app.get("/") 
async def show_unicorn_list(): #this is our function that is below our decorator @app.get("/")
    return {"message": "World!"}


@app.get("/{id}")
async def display_unicorn(id):
   return {"id": id}

@app.post("/")
async def add_unicorn():
    return {"new_unicorn": "new_unicorn"}

@app.put("/{id}")
async def update_unicorn(unicorn_name):
    return {"unicorn_name": unicorn_name}

@app.delete("/{id}")
async def delete_unicorn(unicorn_id):
    return {"unicorn_id": unicorn_id}




