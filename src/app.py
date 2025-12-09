#Kör din FASTAPI-applikation: fastapi dev src/app.py
#Om du vill återkomma till miljön senare och starta virtuella miljö: myenv\Scripts\Activate.ps1
#Avaktivera miljön: deactivate


# -*- coding: utf-8 -*-
#FastAPI is a modern, fast (high-performance), web framework for building APIs with Python based on standard Python type hints.
from fastapi import FastAPI, Header, Request, HTTPException
from unicorns import storage
from unicorns.Unicorn import Unicorn
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
    return unicorn_list    
      
@app.get("/{id}")
async def display_unicorn(id: int, accept: Annotated[str | None, Header()] = None):
    
    unicorn = storage.fetch_unicorn(id) #hämtar en specifik enhörning från unicorn listan. 
   
    #Egentligen behövs Accept-headern inte alls. FastAPI returnerar JSON oavsett.
    if accept == "application/json":
        return unicorn
    else: 
        return None
 
@app.post("/")
async def add_unicorn(unicorn: Unicorn):
    
    """
    Tar emot ett Unicorn-objekt från request-body.
    FastAPI läser JSON som skickas in och skapar ett Unicorn-objekt.

    Anropar storage.add_unicorn(unicorn)
    Detta innebär nästan alltid:

    Spara den nya unicornen i databasen

    Tilldela ett ID, Lagra dess attribut och 
    Returnerar den nyss sparade unicornen som JSON
    """    
    storage.add_unicorn(unicorn)
    return unicorn

@app.put("/{id}")
async def update_unicorn(id:int, unicorn: Unicorn):
    """
    Uppdaterar en befintlig enhörning i databasen.

    Den här funktionen realiserar API-dokumentationens "PUT /<id>".
    Den tar emot en enhörning i request-body (JSON) och ersätter den
    befintliga enhörningen med samma id. Returnerar den uppdaterade enhörningen.
    
    Realisera = implementera eller bygga ut en funktionalitet enligt API-specifikationen
    """
    storage.update_unicorn(id, unicorn)
    return unicorn

@app.delete("/{id}")
async def delete_unicorn(id:int):
    storage.delete_unicorn(id)
    return {"unicorn_id": id}




