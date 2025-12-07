const base = "http://localhost:8000/";
// const innebär att du inte kan ändra värdet. Den är konstant. 
//let tilåter en att ändra värdet. 
// var och let är samma sak. tilåter en att ändra värdet. 

async function listUnicorns()
{
   const Option={
    method: "GET",
    headers: {
        "Accept": "application/json"
    }
   }

   const response = await fetch(base, Option);
   const result = await response.json();
   console.log(result);

   const createUnicornList = document.querySelector("#unicorns");
   createUnicornList.replaceChildren();

   result.forEach((unicorn) =>
    {
        let listitem = document.createElement("li");
        listitem.setAttribute("name", `unicorn_${unicorn.id}`);
        listitem.setAttribute("value", unicorn.id);
        listitem.innerHTML = unicorn.name;
        listitem.addEventListener("click", fetchThenDisplayUnicorn);
        createUnicornList.appendChild(listitem);
   }
) 
}

async function fetchThenDisplayUnicorn(event)
{
    //console.log("Steg A: Klickade på:", event.target.value); // Ska visa ID (t.ex. 5)
    const url = base + event.target.value;
    //motsvarar base + event.target.getAttribute("value");

    const Option={
        method: "GET",
        headers: {
            "Accept": "application/json"
        }
    }

    const response= await fetch(url, Option);
    const result = await response.json();
    console.log(result);

    //console.log("Steg B: Hämtad Enhörningsdata:", result); // SKA VISA DETALJERAD ENHÖRNINGSDATA!

    displayUnicorn(result);
}

async function displayUnicorn(unicorn)
{
    //querySelector kollar upp HTML element, (allt både klass och id) genom CSS-syntax. Måste ha # eller . framför för att leta upp id. 
    //querySelector är mer flexibel och mer kraftfull. 
    //getElementById är begränsad, och kollar upp HTML element genom id. Då behövs inte/ har man ingen # framför. 

    const name = document.querySelector("#unicornName"); 
    const info = document.querySelector("#unicornInfo");
    const image = document.querySelector("#unicornimage");
    const newImage = document.createElement("img");
    newImage.setAttribute("src", unicorn.image);
    const spottedUnicorn = document.querySelector("#unicornSighting");
    
    document.querySelector("#existingUnicorn input[name=id]").value= unicorn.id;
    document.querySelector("#existingUnicorn input[name=name]").value=unicorn.name ;
    document.querySelector("#existingUnicorn input[name=reportedBy]").value=unicorn.reportedBy;
    document.querySelector("#existingUnicorn input[name='spottedWhere.name']").value=unicorn.spottedWhere.name;
    document.querySelector("#existingUnicorn input[name='spottedWhere.lat']").value=unicorn.spottedWhere.lat;
    document.querySelector("#existingUnicorn input[name='spottedWhere.lon']").value=unicorn.spottedWhere.lon;
    document.querySelector("#existingUnicorn input[name=image]").value=unicorn.image;
    document.querySelector("#existingUnicorn textarea[name=description]").value=unicorn.description;

    const date = new Date(unicorn.spottedWhen);
    const formatDate = date.toLocaleDateString('sv-SE', {
        year: "numeric",
        month: '2-digit',
        day: "2-digit"
    });

    document.querySelector("#existingUnicorn input[name=spottedWhen]").value=formatDate;

    name.innerHTML = unicorn.name;
    info.innerHTML = unicorn.description;
    image.replaceChildren(newImage);
    
    //const printText = "Av: " + unicorn.reportedBy + ", " + formatDate + "i " + unicorn.spottedWhere["name"];
    const printText = `Av: ${unicorn.reportedBy}, ${formatDate} i ${unicorn.spottedWhere.name}`;
    spottedUnicorn.innerHTML = printText

}


async function postUnicorn() 
{
    //Skapa en ny enhörning genom att läsa in värdena från formuläret
    const unicorn = buildUnicorn("#newUnicorn")
    
    const Option = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(unicorn)
    };

    //Skicka enhörningen till webbtjänsten

    await fetch(base, Option);

    // Dölj formulären
    hideForms();

    // ... kanske visa om listan till vänster åsse? jajamen
    listUnicorns();
}

async function putUnicorn()
//Uppdaterar enhörningen
{
    const unicorn = buildUnicorn("#existingUnicorn");

    //Uppdatera rätt resurs!
    console.log("hej, jag trodde du hade id", unicorn)
    const url = base + unicorn.id;
    const options = {
        method: "PUT", 
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(unicorn)
    };
    console.log("hej jag vill skicka en förfrågan", url)
    await fetch(url, options);
    //Ladda om sidan
    listUnicorns();
    hideForms();

  
    

}

//Tar bort en enhörning genom att hämta enhörningens id och lägg till det i URL:en
async function deleteUnicorn() 
{
    const url = base + document.querySelector("#existingUnicorn input[name=id]").value;
    const Option = {
        method: "DELETE"
    };

    await fetch(url, Option);

    listUnicorns();

}

function buildUnicorn(formName)
{
    //Med hjälp av strängar skan vi söka efter rätt element
    var unicorn = {
        "id": document.querySelector(formName + " input[name='id']").value,
        "name": document.querySelector(formName + " input[name='name']").value,
        "description": document.querySelector(formName + " textarea[name='description']").value,
        "reportedBy": document.querySelector(formName + " input[name='reportedBy']").value,
        //spottedWhere är ett nästlat objekt
        "spottedWhere": {
            "name": document.querySelector(formName + " input[name='spottedWhere.name']").value,
            "lat": document.querySelector(formName + " input[name='spottedWhere.lat']").value,
            "lon": document.querySelector(formName + " input[name='spottedWhere.lon']").value, 
        },
        "spottedWhen":  document.querySelector(formName + " input[name='spottedWhen']").value,
        "image":        document.querySelector(formName + " input[name='image']").value,
    }
    
    //Ta bort id:t om det inte är definierat och gör det klart för att läggas in i databasen. 
    if (formName == "#newUnicorn") {
        delete(unicorn.id);
    }

    return unicorn;
}

async function hideForms()
{
    // Vi hittar alla formulärelement och applicerar style.display = "none" på
   //   samtliga formulär för att dölja dem genom att använda en forEach(). 

    document.querySelectorAll("form").forEach((form) => {
        form.style.display = "none";
    });

}

async function showAddForm() 
{
   hideForms();

   document.querySelector("#newUnicorn").style.display = "block";
    
   /* Vi väljer ut rätt formulär och visar det genom att applicera
    *  style.display = "block" på det
    */
}

async function showUpdateForm()
{
    hideForms();

    document.querySelector("#existingUnicorn").style.display = "block";

}

// Här kopplar vi ihop funktionerna med respektive knapp
document.querySelector("#addUnicorn").addEventListener("click", showAddForm);
document.querySelector("#updateUnicorn").addEventListener("click", showUpdateForm);
document.querySelector("#postUnicorn").addEventListener("click", postUnicorn);
document.querySelector("#putUnicorn").addEventListener("click", putUnicorn);
document.querySelector("#deleteUnicorn").addEventListener("click", deleteUnicorn);
//Detta är en anynonym funktion. Man använder den endast en gång vid ett tillfälle. 
//unicornList.forEach(element =>
 //   {
        //console.log(element);
 //     createUnicornHTML(listUnicorns, element); 

 //   });
hideForms();
listUnicorns();







