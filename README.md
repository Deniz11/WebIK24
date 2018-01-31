# WebIK24

# Naam applicatie: Moviedatabase

# Leden: Jeroen van Hensbergen, Gino Koppe, Deniz Mermer en Lucas Oud

## Samenvatting

Moviedatabase maakt het in de eerste plaats mogelijk om een lijst aan te maken met al je favoriete films. Daarnaast hebben wij ervoor gezorgd dat er communities aangemaakt kunnen worden waarbij leden films aan die community toe kunnen voegen en comments kunnen plaatsen.
Dit is een uniek idee, omdat het naast een database ook functioneert als een soort sociale media. Gebruikers kunnen namelijk naast het zoeken van hun favoriete films lijsten bijhouden en die met andere filmliefhebbers delen.

## Schetsen

Homepage:
[![https://gyazo.com/d040afd103907e5964607e7ef9e838ad](https://i.gyazo.com/d040afd103907e5964607e7ef9e838ad.png)](https://gyazo.com/d040afd103907e5964607e7ef9e838ad)

## Features

<ol>
<li>Gebruikers kunnen accounts aanmaken en inloggen</li>
<li>Gebruikers kunnen community's volgen en aanmaken</li>
<li>Gebruikers kunnen naar films, community's en acteurs zoeken via de API/database met een id of naam</li>
<li>Gebruikers kunnen films toevoegen aan een persoonlijke lijst</li>
<li>Gebruikers kunnen gegevens wijzigen, zoals het wachtwoord of hun gehele account verwijderen</li>
<li>Gebruikers kunnen hun eigen items aan een community toevoegen.</li>
<li>Gebruikers kunnen comments plaatsen onder community's</li>
</ol>

# Afhankelijkheden

## Databronnen
Als datasource maken we gebruik van de API van <a href="https://github.com/richardasaurus/imdb-pie">IMDBpie</href>. Hieruit hebben wij functies gebruikt om films op te halen uit de database (incl. plaatjes)

## Externe componenten
Een open source SQL applicatie (SQLlite) voor het beheren van de zoekfunctionaliteit. Flask voor het framework van de website.

## Concurrerende bestaande sites
In het geval van films is www.imdb.com de grootste en meest bekende concurrent. Wij doelen op een meer simpele uitvoering van IMDb.

# Taakverdeling
<ol>
<li>Jeroen</li>
Jeroen heeft veel gedaan aan het maken van functies met betrekking tot de IMDbpie. Hij heeft gezorgd dat de films worden weergegeven op de homepagina en communitypagina.
Zijn taak was tevens om de functies in communities.py te maken. Hiermee werd het mogelijk om communities te maken, weer te geven en te wijzigen. Hij heeft zich verdiept in Javascript om de homepagina mooi te maken.
<li>Lucas</li>
Lucas heeft gezorgd voor het uiterlijk van de tabellen en heeft met name tijd besteed aan de User class. Daarnaast heeft hij gezorgd voor de functionaliteit en uiterlijk van de
login, register en user settings pagina. Ook heeft hij de navbar werkend gemaakt met de search class.
<li>Deniz</li>
Deniz heeft ervoor gezorgd dat de zoekfunctie de benodigde informatie uit de IMDb database haalt. Hierbij behoren de functies uit search.py.
Dit was een lastige klus en heeft veel tijd gekost. Hij heeft geholpen met de functies van Gino en Lucas. Uiteindelijk zorgde hij er ook voor dat het mogelijk werd gemaakt om op acteurnaam te zoeken.
<li>Gino</li>
Gino kreeg de taak om persoonlijke lijsten aan te maken en daar films aan toe te kunnen voegen. Daarnaast heeft hij gewerkt aan het uiterlijk van de website. Ook heeft hij gewerkt aan de commentsectie, zodat
gebruikers comments kunnen plaatsen onder een community.
</ol>

# Repository
In de map Collectionneur staat alles wat betrekking heeft op het uiterlijk van de website. We hebben een map gemaakt genaamd static waarin de css van onze website grotendeels staat. Door een tijdgebrek hebben wij niet alle css in de map kunnen zetten, waardoor er nog wat losse dingen bovenaan de html staat.
Daarnaast hebben we een map met templates, waarin alle html pagina's staan van onze website. Daarnaast staan al onze classes en functies in de map Collectionneur.

## Classes en functies

### application.py
Hierin staan de routes van alle websites. Dit is in principe de controller van de website. Hierin worden websites en functies aangeroepen.
### communities.py
Hierin staan alle functies waarmee communities gemaakt en bewerkt kunnen worden. Daarnaast staan er functies in die betrekking hebben op de leden van de website.
### helpers.py
Hierin staan functies die ervoor zorgen dat een id gevalideerd kan worden.
### homepage.py
Hier staan functies die ervoor zorgen dat films en community's weergegeven kunnen worden op de homepagina.
### lists.py
Hierin bevinden zich functies om lijsten aan te maken en te bewerken.
### search.py
Hierin bevinden zich functies om items op te halen uit de IMDb database. Daarnaast kan er op acteurs of communities worden gezocht.
### user.py
Hierin staan functies om een account aan te maken, te verwijderen of te bewerken (wachtwoord veranderen)

