#Kör din FASTAPI-applikation: fastapi dev src/app.py
#Om du vill återkomma till miljön senare och starta virtuella miljö: myenv\Scripts\Activate.ps1
#Avaktivera miljön: deactivate


# -*- coding: utf-8 -*-
#FastAPI is a modern, fast (high-performance), web framework for building APIs with Python based on standard Python type hints.
from fastapi import FastAPI, Header, Request
from unicorns import storage
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware #Vi importerar CORSmiddleware för att fixa "CORS" error

app = FastAPI()

# CORS (cross origin request sharing) middleware för cors error handeling
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

#Det här nollställer databasen inför varje körning
storage.setup()

#path is / and operation is GET
"""@app.get("/")
async def show_unicorn_list(request: Request, response: Response):
    
    # NOTE: vi sköter detta vid "app.add_middleware" för alla platser (inklusive denna) istället
    # Tillåt åtkomst från alla platser (aka origins), t.ex. min html-fil eller från en annan webbplats
    # response.headers['Access-Control-Allow-Origin'] = "*"
    
    # Dubbelkolla att dom skickade med Accept-headern för JSON
    if request.headers['Accept'] == 'application/json':
        unicorns = storage.fetch_unicorns()
        return unicorns
    else:
        return None"""

#Detta är min funktion och ovanför är min decorator @app.get("/")
@app.get("/")
async def show_unicorn_list(request: Request, accept: Annotated[str | None, Header()] = None):
    """
    @app.get: Detta är en router-deklaration som talar om för FastAPI att den inkommande funktionen ska köras när servern får en HTTP-begäran av typen GET.

    ("/") :	Detta anger stigen (path) eller slutpunkten (endpoint) för begäran. / är rotstigen, 
    vilket betyder att funktionen körs när en användare besöker t.ex. http://localhost:8000/.

    async def: Betyder att funktionen är en asynkron funktion. 
    FastAPI: bygger på async/await och det gör att din applikation kan hantera många samtidiga anrop utan att blockeras (vänta) medan den t.ex. hämtar data från en databas (storage.fetch_unicorns()).

    request: Namnet på variabeln i din funktion.
    Request: Typ-hänvisning som talar om för FastAPI att funktionen behöver det fullständiga Request-objektet från det inkommande anropet. 
    Detta objekt innehåller all information om anropet: headers, cookies, URL-parametrar, etc. Den kan användas för att rendera HTML-mallar.

    accept:	Namnet på variabeln i din funktion.
    : Annotated[...]: Denna del är en avancerad Python-funktion som låter dig lägga till metadata till typ-hänvisningar.

    Header(): Detta är metadatan som talar om för FastAPI att den inte ska leta efter värdet i t.ex. URL:en eller i begärandets kropp (body), 
    utan specifikt i HTTP-headern med samma namn (Accept). 
    FastAPI är smart nog att läsa in Accept-headern i en variabel som heter accept.

    =None:	Gör parametern valfri. Om klienten inte skickar med en Accept-header, kommer variabeln accept att få värdet None istället för att funktionen kraschar.
    """
    unicorns = storage.fetch_unicorns()
    unicorn_list = []
    for unicorn in unicorns:
        unicorn_list.append(
            { 
            "id": unicorn.id,
            "name": unicorn.name,
            "details": "http://localhost:8000/" + str(unicorn.id)   
            })  
    """
        unicorn_list.append() Lägger till formaterad data. För varje enhörning i loopen skapas ett nytt dictionary (objekt i JSON-termer)
        med exakt de tre nycklarna (id, name, details) som API:et ska returnera.
    """    
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




