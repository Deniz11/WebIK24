# WebIK24

# Naam applicatie: Collectioneur

# Leden: Jeroen van Hensbergen, Gino Koppe, Deniz Mermer en Lucas Oud

## Samenvatting

Het huidige idee is om het mogelijk te maken voor mensen om lijstjes te maken met voorkeuren en in een later stadium subgroepen te maken om mensen met gelijke interesses te koppelen. Denk hierbij aan een auto- of filmdatabase. Mensen kunnen elkaar tips geven en in een subgroep discussieren over hun favoriete automerk. Dit is een uniek idee, omdat het naast een database ook functioneert als een soort sociale media. Gebruikers kunnen namelijk naast het zoeken van hun favoriete auto's ook connecties maken met mensen met dezelfde interesse(s) en hun kennis opnemen.

## Schetsen

Homepage:
[![https://gyazo.com/f849a7936943fa6a8687833fd3029c26](https://i.gyazo.com/f849a7936943fa6a8687833fd3029c26.png)](https://gyazo.com/f849a7936943fa6a8687833fd3029c26)

Zoekpagina:
[![https://gyazo.com/be7deeb5d74d860c2353a1327e7e595f](https://i.gyazo.com/be7deeb5d74d860c2353a1327e7e595f.png)](https://gyazo.com/be7deeb5d74d860c2353a1327e7e595f)

Profielpagina:
[![https://gyazo.com/7bdf0e592bcbc366e4c2e44418d3b77e](https://i.gyazo.com/7bdf0e592bcbc366e4c2e44418d3b77e.png)](https://gyazo.com/7bdf0e592bcbc366e4c2e44418d3b77e)

Resultaten:
[![https://gyazo.com/80a5a05d38cf83f7807976d2f83b2cb5](https://i.gyazo.com/80a5a05d38cf83f7807976d2f83b2cb5.png)](https://gyazo.com/80a5a05d38cf83f7807976d2f83b2cb5)

lijstpagina:
[![https://gyazo.com/bc0b20cf2feb20e5e09ee85dbe0b3a27](https://i.gyazo.com/bc0b20cf2feb20e5e09ee85dbe0b3a27.png)](https://gyazo.com/bc0b20cf2feb20e5e09ee85dbe0b3a27)

Iteminformatie:
[![https://gyazo.com/dd23d6edbff9dc5c80c50d39901d31ea](https://i.gyazo.com/dd23d6edbff9dc5c80c50d39901d31ea.png)](https://gyazo.com/dd23d6edbff9dc5c80c50d39901d31ea)

Groeppagina:
[![https://gyazo.com/b382061bd1b8053ef143eb5a135df158](https://i.gyazo.com/b382061bd1b8053ef143eb5a135df158.png)](https://gyazo.com/b382061bd1b8053ef143eb5a135df158)

Sitemap:
[![https://gyazo.com/d30130e5c9b1304a2b35175e7020ed83](https://i.gyazo.com/d30130e5c9b1304a2b35175e7020ed83.png)](https://gyazo.com/d30130e5c9b1304a2b35175e7020ed83)


## Features

### Minimum viable product

<ol>
<li>Gebruikers kunnen een account aanmaken en inloggen</li>
<li>Gebruikers kunnen community's (subgroepen) volgen en aanmaken</li>
<li>Gebruikers kunnen naar films en community's zoeken via de API/database met een id of exacte naam</li>
<li>Gebruikers kunnen films toevoegen aan een persoonlijke lijst</li>
<li>Gebruikers kunnen aan films gerelateerde community's zien</li>
<li>Gebruikers kunnen gegevens wijzigen, zoals het wachtwoord of hun gehele account verwijderen</li>
</ol>

### Extra's

<ol>
<li>Gebruikers kunnen andere gebruikers opzoeken</li>
<li>Gebruikers kunnen items delen met andere gebruikers</li>
<li>Gebruikers kunnen andermans lijsten bekijken.</li>
<li>Gebruikers kunnen hun eigen items aan een community toevoegen.</li>
<li>Gebruikers kunnen comments plaatsen onder subgroepen, profielen en individuele items.</li>
<li>Gebruikers kunnen andere gebruikers berichten sturen</li>
<li>Gebruikers kunnen zien hoe vaak een item is toegevoegd aan een lijst.</li>
<li>Gebruikers kunnen items, lijsten en andere gebruikers volgen en krijgen notificaties wanneer deze worden geüpdatet.</li>
</ol>

## Afhankelijkheden

Nu je dit hebt gedaan (en je hebt inmiddels ook een beetje een beeld van hoe webapplicaties in elkaar zitten) kun je een eerste lijst van afhankelijkheden maken: dingen die je niet zelf programmeert maar wel moet gebruiken, begrijpen of regelen.

### Databronnen
Als datasource maken we gebruik van de API van http://edmunds.mashery.com/ indien we voor een autodatabase kiezen. Er bestaat een mogelijkheid dat het technisch niet haalbaar is. Onze tweede keuze is www.emdb.com als API voor een film database.

Update: we hebben besloten om de api van The Movie Database the gebruiken. link: https://www.themoviedb.org/documentation/api

### Externe componenten
Een open source SQL applicatie voor het beheren van de zoekfunctionaliteit. Flask voor het framework van de website.

### Concurrerende bestaande sites
In het geval van films is www.imdb.com de grootste en meest bekende concurrent. Wij doelen op een meer simpele uitvoering van imdb.

### Moeilijkste delen
Het implementeren van sociale contacten. Hoe laat je gebruikers communiceren en een subgroep beheren. Het maken van een goede zoekpagina is ook lastig. Welke velden zijn cruciaal? Hoe zoekt de site nou echt in de API?