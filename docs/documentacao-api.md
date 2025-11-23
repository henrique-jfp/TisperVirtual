21/11/2025, 04:41 API-Football - Documentation

# API-FOOTBALL (3.9.3)

[support: https://dashboard.api](mailto:https://dashboard.api-football.com) ~~-~~ football.com | URL: [https://www.api](https://www.api-football.com/) ~~-~~ football.com

# Introduction

Welcome to Api ~~-~~ Football! You can use our API to access all API endpoints, which can get information

about Football Leagues & Cups.

We have language bindings in C, C#, cURL, Dart, Go, Java, Javascript, NodeJs, Objective ~~-~~ c, OCaml, Php,

PowerShell, Python, Ruby, Shell and Swift! You can view code examples in the dark area to the right,

and you can switch the programming language of the examples with the tabs in the top right.

The update frequency indicated in the documentation is given as an indication and may vary for certain

We uses API keys to allow access to the API. You can register a new API key in our [dashboard.](https://dashboard.api-football.com/register)


API-SPORTS : [https://v3.football.api](https://v3.football.api-sports.io/) ~~-~~ sports.io/

Our API expects for the API key to be included in all API requests to the server in a header that looks

like the following:

Make sure to replace `XxXxXxXxXxXxXxXxXxXxXxXx` with your API key.

REQUESTS HEADERS & CORS

The API is configured to work only with GET requests and allows only the headers listed below:

```
      x-apisports-key
```

If you make non ~~-~~ GET requests or add headers that are not in the list, you will receive an error from the

API.

Some frameworks (especially in JS, nodeJS..)automatically add extra headers, you have to make sure

to remove them in order to get a response from the API.


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 1/130


21/11/2025, 04:41 API-Football - Documentation
## API-SPORTS Account

If you decided to subscribe directly on our site, you have a dashboard at your disposal at the following

It allows you to:

To follow your consumption in real time

it


Manage your subscription and change it if necessary

Check the status of our servers

Test all endpoints without writing a line of code.

You can also consult all this information directly through the API by calling the endpoint `status` .

This call does not count against the daily quota.





































Headers sent as response

When consuming our API, you will always receive the following headers appended to the response:


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 2/130


21/11/2025, 04:41 API-Football - Documentation

`x-ratelimit-requests-limit` : The number of requests allocated per day according to your

`x-ratelimit-requests-remaining` : The number of remaining requests per day according to

`X-RateLimit-Limit` : Maximum number of API calls per minute.

`X-RateLimit-Remaining` : Number of API calls remaining before reaching the limit per minute.

Rate Limiting Policy

If you exceed your allowed request rate per minute, either through continuous excessive usage or by

generating abnormal traffic spikes, your access may be temporarily or permanently blocked by our

firewall without prior notice. This ensures service stability and fair usage for all customers.


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 3/130


21/11/2025, 04:41 API-Football - Documentation

Live tester

# Architecture
# Logos / Images

Calls to logos/images do not count towards your daily quota and are provided for free. However these

it


calls are subject to a rate per second & minute, it is recommended to save this data on your side in


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 4/130


21/11/2025, 04:41 API-Football - Documentation

order not to slow down or impact the user experience of your application or website. For this you can

use CDNs such as [bunny.net.](https://bunny.net/?ref=8r6al7jhm4)

We have a tutorial available [here,](https://www.api-football.com/news/post/optimizing-sports-websites-bunnycdn-api-sports-image-storage-guide) which explains how to set up your own media system with

Logos, images and trademarks delivered through the API are provided solely for identification and
descriptive purposes (e.g., identifying leagues, teams, players or venues). We does not own any of

these visual assets, and no intellectual property rights are claimed over them. Some images or data
may be subject to intellectual property or trademark rights held by third parties (including but not
limited to leagues, federations, or clubs). The use of such content in your applications, websites, or

products may require additional authorization or licensing from the respective rights holders. You are

fully responsible for ensuring that your usage of any logos, images, or branded content complies with

applicable laws in your country or the countries where your services are made available. We are not

affiliated with, sponsored by, or endorsed by any sports league, federation, or brand featured in the data

# Sample Scripts

Here are some examples of how the API is used in the main development languages.

You have to replace `{endpoint}` by the real name of the endpoint you want to call, like `leagues` or

`fixtures` for example. In all the sample scripts we will use the `leagues` endpoint as example.

Also you will have to replace `XxXxXxXxXxXxXxXxXxXxXx` with your API ~~-~~ KEY provided in the

## C

```
    libcurl

```
















https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 5/130


21/11/2025, 04:41 API-Football - Documentation










## C#

```
RestSharp

```



















## cURL

```
Curl

```





## Dart

```
http

```










https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 6/130


21/11/2025, 04:41 API-Football - Documentation























 

```
Native

```
















https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 7/130


21/11/2025, 04:41 API-Football - Documentation












```
OkHttp

```















```
Unirest

```









```
Fetch

```














https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 8/130


21/11/2025, 04:41 API-Football - Documentation








```
jQuery

```











```
XHR

```











```
    Axios

```

https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 9/130


21/11/2025, 04:41 API-Football - Documentation


















```
Native

```






























https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 10/130


21/11/2025, 04:41 API-Football - Documentation






```
Requests

```











```
Unirest

```



















```
NSURLSession

```












https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 11/130


21/11/2025, 04:41 API-Football - Documentation
























## OCaml

```
Cohttp

```


















https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 12/130


21/11/2025, 04:41 API-Football - Documentation

## Php

```
    cURL

```





































```
Request2

```






























https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 13/130


21/11/2025, 04:41 API-Football - Documentation














```
Http

```















```
RestMethod

```



```
http.client

```




https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 14/130


21/11/2025, 04:41 API-Football - Documentation










```
Requests

```















## Ruby

```
Net::HTTP

```










https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 15/130


21/11/2025, 04:41 API-Football - Documentation

```
    Httpie

```











```
wget

```











```
URLSession

```








https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 16/130


21/11/2025, 04:41 API-Football - Documentation



















3.9.3

Add endpoint `players/profiles` that returns the list of all available players

Add endpoint `players/teams` that returns the list of teams and seasons in which the player

played during his career

Endpoint `fixtures`

Endpoint `fixtures/rounds`

Add the `dates` parameter that allows to retrieve the dates of each round in the response

Endpoint `fixtures/statistics`

Add the `half` parameter that allows to retrieve the halftime statistics in the response

Endpoint `injuries`

Add the `ids` parameter that allows to retrieve data from several fixtures in one call

Endpoint `teams/statistics`, more statistics added

Goals Over

Goals Under

Endpoint `sidelined`

Add the `players` and `coachs` parameters that allows to retrieve data from several

players/coachs in one call

Endpoint `trophies`


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 17/130


21/11/2025, 04:41 API-Football - Documentation

Add the `players` and `coachs` parameters that allows to retrieve data from several

players/coachs in one call


3.9.2

Endpoint `odds`

Endpoint `teams`

Add parameter `code`

Add parameter `venue`

Endpoint `fixtures`

Add the `ids` parameter that allows to retrieve data from several fixtures including events,

lineups, statistics and players in one Api call

Add the Possibility to add several status for the `status` parameter

Add parameter `venue`

Endpoint `fixtures/headtohead`

Add the Possibility to add several status for the `status` parameter

Add parameter `venue`


3.8.1

Endpoint `fixtures/lineups`

Add players positions on the grid

Add players' jerseys colors

Endpoint `fixtures/events`

add VAR events

Endpoint `teams`

Add tri ~~-~~ code

Endpoint `teams/statistics`, more statistics added

Scoring minute

Cards per minute

Most played formation

Penalty statistics

Add Coaches Photos


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 18/130


21/11/2025, 04:41 API-Football - Documentation

# CDN
# Optimizing Sports Websites with BunnyCDN

BunnyCDN is a Content Delivery Network (CDN)that delivers a global content distribution experience.

With strategically positioned servers, BunnyCDN ensures swift and reliable delivery of static content,

optimizing website performance with features like intelligent image optimization, sophisticated

caching, and advanced security measures.

Unlocking Media Delivery Excellence with BunnyCDN:

Quick Configuration: Set up your media CDN in just 5 minutes. Define cache times, customize your

~~–~~
domain it's that simple.

Global Accessibility: Leverage BunnyCDN's expansive server network for swift and dependable

Customized Configuration: Tailor caching, define cache times, and implement CORS headers to

create an efficient and seamless user experience.

Own Your Domain: Personalize your media delivery with your domain, enhancing your brand's

online presence.

Robust Security: BunnyCDN integrates advanced security features, guaranteeing a secure

environment for delivering your content.

Responsive Performance: Experience responsive performance without the need for prior media

downloads. Discover the capabilities of BunnyCDN for optimized media delivery.

A tutorial is available [here](https://www.api-football.com/news/post/optimizing-sports-websites-bunnycdn-api-sports-image-storage-guide) on our blog to help you configure it.

# Databases Solutions


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 19/130


21/11/2025, 04:41 API-Football - Documentation
# Enhance Your Data Management with Aiven

Integrating databases into your application can greatly enhance data management and storage. If

you're looking for high ~~-~~ performing, flexible, and secure database solutions, we recommend checking

out [Aiven.](https://aiven.io/?utm_source=website&utm_medium=referral&utm_campaign=api_football)

Aiven is a cloud platform that offers a range of managed database services, including relational

databases, NoSQL databases, streaming data processing systems, and much more. Their offerings

include `PostgreSQL`, `MySQL`, `Cassandra`, `Redis`, `Kafka`, and many other databases, all with

simplified management, high availability, and advanced security.

Moreover, Aiven provides a free tier to get started, along with testing credits to explore their offerings.

it


This opportunity allows you to evaluate their platform and determine if it meets your needs.

One particularly attractive feature of Aiven is that they work with multiple cloud providers, including

`Google Cloud`, `Amazon Web Services (AWS)`, `Microsoft Azure`, `DigitalOcean`, and more.

This means you have the flexibility to choose the best cloud infrastructure for your project.

In terms of reliability, Aiven is committed to providing a 99.99% Service Level Agreement (SLA),

ensuring continuous and highly available service.

To test their services, visit this [page.](https://console.aiven.io/signup?utm_source=website&utm_medium=referral&utm_campaign=api_football)

If you're a developer, explore their DEV [center](https://aiven.io/developer?utm_source=website&utm_medium=referral&utm_campaign=api_football) for technical information.

Check out Aiven's [documentation](https://docs.aiven.io/?utm_source=website&utm_medium=referral&utm_campaign=api_football) for detailed information on their services and features.

By integrating Aiven with our API, you can efficiently store, manage, and analyze your data while taking

advantage of their cloud database solutions' flexibility and scalability.
# Real-Time Data Management with Firebase

When you're looking for a real ~~-~~ time data management solution for your application, [Firebase's](https://firebase.google.com/products/realtime-database/?utm_source=api-football) Realtime

[Database](https://firebase.google.com/products/realtime-database/?utm_source=api-football) is a powerful choice. Explore how Firebase can enhance real ~~-~~ time data management for your

Firebase's [Realtime](https://firebase.google.com/products/realtime-database/?utm_source=api-football) Database offers a cloud ~~-~~ based real ~~-~~ time database that synchronizes data in real ~~-~~

it


time across users and devices. This makes it an ideal choice for applications that require instant data

Why Choose Firebase's Realtime Database?


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 20/130


21/11/2025, 04:41 API-Football - Documentation

Real-Time Data: Firebase allows you to store real ~~-~~ time data, meaning that updates are instantly

propagated to all connected users.

Easy Synchronization: Data is automatically synchronized across all devices, providing a

consistent and real ~~-~~ time user experience.

Built-In Security: Firebase offers flexible security rules to control data access and ensure privacy.

Simplified Integration: Firebase's Realtime Database easily integrates with other Firebase

services, simplifying backend management.

Helpful Links:

Explore Firebase's [Realtime](https://firebase.google.com/products/realtime-database/) Database: Discover the features and advantages of Firebase's

Realtime Database for efficient real ~~-~~ time data management.

Firebase's Realtime [Database](https://firebase.google.com/docs/database/) Documentation: Refer to the comprehensive documentation for

Firebase's Realtime Database for a smooth integration.

A tutorial describing each step is available on our blog [here.](https://www.api-football.com/news/post/how-to-use-firebase-with-api-football-real-time-data-integration)

API ~~-~~ SPORTS widgets allow you to easily display dynamic sports data on your website.

They are designed to be:

Ultra-modular: each component is autonomous

Customisable: language, theme, content, behaviour

Easy to integrate: no framework required, a simple HTML tag is all you need

They use request from your API ~~-~~ SPORTS account and work with all plans, including the free plan.

Find all the documentation on widgets [here](https://api-sports.io/documentation/widgets/v3)


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 21/130


21/11/2025, 04:41 API-Football - Documentation

## Security

Our widgets use your account's API ~~-~~ KEY, which must be specified in the `data-key` attribute of your

it



When using these widgets it is important to be aware that your API ~~-~~ KEY will be visible to the users of

it


your site, it is possible to protect yourself from this by allowing only the desired domains or IP in our

[dashboard.](https://dashboard.api-football.com/profile?access) This way no one else can use your API ~~-~~ KEY for you. If you have already set up your widget

and have not activated this option, you can reset your API ~~-~~ KEY and activate this option after.

You can further enhance security by completely hiding your API ~~-~~ KEY from the source code by following

this [tutorial.](https://www.api-football.com/news/post/how-to-optimize-widgets-cache-and-security-tutorial)

By using Widgets, each visit to a page on your website triggers one or more API requests to retrieve

data. Without a caching system, your daily quota can be reached very quickly.

Example: If a page triggers a single API request per visitor and you receive 80 visits to that page in one

minute, this results in 80 API requests. Over a full day, that can add up to 115 200 requests.

By implementing a caching system, even with a very short duration, such as 60 seconds, you can

drastically reduce the number of requests. The first visit will trigger an API request, but the response

will then be cached for the next 60 seconds. This means that if 80 visitors access the same page


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 22/130


21/11/2025, 04:41 API-Football - Documentation

within that time frame, only the first request will reach the API, while the next 79 will be served directly

from the cache.

With this system in place, you reduce usage from 115 200 requests per day to just 1 440.

A full tutorial is available [here,](https://www.api-football.com/news/post/how-to-optimize-widgets-cache-and-security-tutorial) explaining step by step how to set up an effective caching system.

it



If the widget does not display the requested information, it is possible to set the `data-show-errors`

tag to true to display error messages directly in the widget and in the console. This can be due to
several things like : (No ~~n-e~~ xhaustive list)

You have reached your daily number of requests

Tags are incorrectly filled in

Your API ~~-~~ KEY is incorrect
## All available widgets

Below is a list of all available widgets:

`games` → list of matches

`game` → details of a match

`team` → team profile

`player` → player profile

`standings` → league table

`league` → schedule

`leagues` → list of all leagues

`h2h` → historical head ~~-~~ to ~~-~~ head

`races`, `race`, `driver` → Formula 1


`fights`, `fight`, `fighter` → MMA

Each widget adapts automatically based on the selected sport.
# Before You Begin


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 23/130


21/11/2025, 04:41 API-Football - Documentation

## Dynamic targeting

Some widgets, such as `games`, can dynamically open other widgets like `game`, `standings`,

`player`, and more.

This interaction is enabled using the `data-target-*` attributes.

These attributes allow you to define where the opened widget should be rendered:

`modal` → renders the widget inside a modal.

CSS selector ( `#id` or `.class` ) → injects the widget into a specific HTML element on the page.

These targeting options are available for:

General sports widgets (Football, Basketball, etc.):

```
      data-target-game

      data-target-standings

      data-target-team

      data-target-player

      data-target-league
```

Formula 1 specific:

```
      data-target-race

      data-target-ranking

      data-target-driver

      data-target-fight

      data-target-fighter
```

Target a container by ID





















Target using modal


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 24/130


21/11/2025, 04:41 API-Football - Documentation










## Language

The `data-lang` attribute allows you to easily switch the interface language of all widgets.

Available languages:

Example usage

















https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 25/130


21/11/2025, 04:41 API-Football - Documentation

Custom translations:

For complete control over wording, you can load your own translation file using `data-custom-lang` .

This file must be a valid JSON object following the internal key structure.

You can download the translation file [here.](https://widgets.api-sports.io/3.1.0/en.json)

It allows you to:

Override specific labels

Translate missing terms

Adapt terminology to your audience

Example JSON format:















You can use `data-lang` and `data-custom-lang` together.

If a key is defined in both, the custom file will take priority.

Exemple for custom translation







https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 26/130


21/11/2025, 04:41 API-Football - Documentation





You have a tutorial available [here](https://www.api-football.com/news/post/create-a-custom-translation-file-for-your-widgets)


 
## Predefined themes

Four built ~~-~~ in themes are available by default. You can set them using the `data-theme` attribute on

`white` (default)

```
      grey

      dark

      blue
```

Each theme adjusts background colors, text colors, button styles, borders, and more.

White Dark


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 27/130


21/11/2025, 04:41 API-Football - Documentation

Grey Blue
## Custom theme

You can override the default styles by creating your own CSS theme using the `data-theme` attribute

and custom variable declarations.





































https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 28/130


21/11/2025, 04:41 API-Football - Documentation







































Find all the documentation on widgets [here](https://api-sports.io/documentation/widgets/v3)

# Timezone

Get the list of available timezone to be used in the fixtures endpoint.

This endpoint does not require any parameters.

it



Update Frequency : This endpoint contains all the existing timezone, it is not updated.

Recommended Calls : 1 call when you need.


HEADER PARAMETERS


```
x-apisports-key

required

```




https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 29/130


21/11/2025, 04:41 API-Football - Documentation


**200** OK

**204** No Content

**499** Time Out

**500** Internal Server Error

GET `/timezone`

Request samples

Php Python Node JavaScript Curl Ruby

```
     $client = new http Client\ ;

     $request = new http Client Request\ \ ;

     $request->setRequestUrl 'https://v3.football.api-sports.io/timezone'( );

     $request->setRequestMethod 'GET'( );

     $request->setHeaders array( (

          'x-apisports-key' => 'XxXxXxXxXxXxXxXxXxXxXxXx'

     ));

     $client->enqueue $request ->( ) send();

```



```
$response = $client->getResponse

```

```
();

```

```
  echo $response->getBody
```

Response samples


```
();

```


200 204 499 500

```
{

  "get": "timezone",

  "parameters": [ ],

```


Copy Expand all Collapse all



https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 30/130


21/11/2025, 04:41 API-Football - Documentation

```
       "errors": [ ],

       "results": 425,

             "paging": {

         "current": 1,

         "total": 1

       },

      - "response": [

         "Africa/Abidjan",

         "Africa/Accra",

         "Africa/Addis_Ababa",

         "Africa/Algiers",

         "Africa/Asmara"

       ]

     }

# Countries

## Countries
```

Get the list of available countries for the `leagues` endpoint.

The `name` and `code` fields can be used in other endpoints as filters.

To get the flag of a country you have to call the following url: `https://media.api-`

```
    sports.io/flags/{country_code}.svg
```

Examples available in Request samples "Use Cases".

All the parameters of this endpoint can be used together.

Update Frequency : This endpoint is updated each time a new league from a country not covered by

the API is added.

Recommended Calls : 1 call per day.

QUERY PARAMETERS


```
name

```


The name of the country



https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 31/130


21/11/2025, 04:41 API-Football - Documentation


```
  code

  search

```

HEADER PARAMETERS

```
  x-apisports-key

  required

```

**200** OK

**204** No Content

**499** Time Out



string [ 2 .. 6 ] characters FR, GB ~~-~~ ENG, IT…

The Alpha code of the country

The name of the country



**500** Internal Server Error

GET `/countries`

Request samples

Use Cases Php Python Node JavaScript Curl Ruby

```
  // Get all available countries across all {seasons} and competitions

```



```
     get "https://v3.football.api-sports.io/countries"( );

     // Get all available countries from one country {name}

     get "https://v3.football.api-sports.io/countries?name=england"( );

     // Get all available countries from one country {code}

     get "https://v3.football.api-sports.io/countries?code=fr"( );

     // Allows you to search for a countries in relation to a country {name}

     get "https://v3.football.api-sports.io/countries?search=engl"( );

```

https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 32/130


21/11/2025, 04:41 API-Football - Documentation

Response samples

200 204 499 500

Copy Expand all Collapse all

```
     {

       "get": "countries",

      - "parameters": {

         "name": "england"

       },

       "errors": [ ],

       "results": 1,

             "paging": {

         "current": 1,

         "total": 1

       },

      - "response": [

        + { … }

       ]

     }

# Leagues

## Leagues
```

Get the list of available leagues and cups.

it



The league `id` are unique in the API and leagues keep it across all `seasons`

To get the logo of a competition you have to call the following url: `https://media.api-`

```
    sports.io/football/leagues/{league_id}.png

it

```

This endpoint also returns the `coverage` of each competition, which makes it possible to know what

is available for that league or cup.


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 33/130


21/11/2025, 04:41 API-Football - Documentation

The values returned by the coverage indicate the data available at the moment you call the API, so for a

it


competition that has not yet started, it is normal to have all the features set to `False` . This will be

updated once the competition has started.

You can find all the leagues ids on our [Dashboard.](https://dashboard.api-football.com/soccer/ids)















In this example we can deduce that the competition does not have the following features:

it



`statistics_fixtures`, `statistics_players`, `odds` because it is set to `False` .

The coverage of a competition can vary from season to season and values set to `True` do not

guarantee 100% data availability.

Some competitions, such as the `friendlies`, are exceptions to the coverage indicated in the

`leagues` endpoint, and the data available may differ depending on the match, including livescore,

events, lineups, statistics and players.

Competitions are automatically renewed by the API when a new season is available. There may be a

delay between the announcement of the official calendar and the availability of data in the API.

For `Cup` competitions, fixtures are automatically added when the two participating teams are known.

For example if the current phase is the 8th final, the quarter final will be added once the teams playing

this phase are known.

Examples available in Request samples "Use Cases".

Most of the parameters of this endpoint can be used together.

Update Frequency : This endpoint is updated several times a day.

Recommended Calls : 1 call per hour.

QUERY PARAMETERS


```
id

```


The id of the league



https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 34/130


21/11/2025, 04:41 API-Football - Documentation


```
  name

  country

  code

  season

  team

  type

  current

  search

  last

```

HEADER PARAMETERS

```
  x-apisports-key

  required

```

**200** OK

**204** No Content

**499** Time Out



The name of the league

The country name of the league

string [ 2 .. 6 ] characters FR, GB ~~-~~ ENG, IT…

The Alpha code of the country

integer = 4 characters YYYY

The season of the league

The id of the team

Enum: `"league"` `"cup"`

The type of the league

string Return the list of active seasons or the las... Show pattern

Enum: `"true"` `"false"`

The state of the league

The name or the country of the league

The X last leagues/cups added in the API



**500** Internal Server Error


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 35/130


21/11/2025, 04:41 API-Football - Documentation

GET `/leagues`

Request samples

Use Cases Php Python Node JavaScript Curl Ruby

```
     // Allows to retrieve all the seasons available for a league/cup

     get "https://v3.football.api-sports.io/leagues?id=39"( );

     // Get all leagues from one league {name}

     get "https://v3.football.api-sports.io/leagues?name=premier league"( );

     // Get all leagues from one {country}

     // You can find the available {country} by using the endpoint country

```



```
     get "https://v3.football.api-sports.io/leagues?country=england"( );

     // Get all leagues from one country {code} (GB, FR, IT etc..)

     // You can find the available country {code} by using the endpoint country

     get "https://v3.football.api-sports.io/leagues?code=gb"( );

     // Get all leagues from one {season}

     // You can find the available {season} by using the endpoint seasons

     get "https://v3.football.api-sports.io/leagues?season=2019"( );

     // Get one league from one league {id} & {season}

     get "https://v3.football.api-sports.io/leagues?season=2019&id=39"( );

     // Get all leagues in which the {team} has played at least one match

     get "https://v3.football.api-sports.io/leagues?team=33"( );

     // Allows you to search for a league in relation to a league {name} or {count

     get "https://v3.football.api-sports.io/leagues?search=premier league"( );

     get "https://v3.football.api-sports.io/leagues?search=England"( );

     // Get all leagues from one {type}

     get "https://v3.football.api-sports.io/leagues?type=league"( );

     // Get all leagues where the season is in progress or not

     get "https://v3.football.api-sports.io/leagues?current=true"( );

     // Get the last 99 leagues or cups added to the API

     get "https://v3.football.api-sports.io/leagues?last=99"( );

     // It’s possible to make requests by mixing the available parameters

     get "https://v3.football.api-sports.io/leagues?season=2019&country=england&ty(

```

https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 36/130


21/11/2025, 04:41 API-Football - Documentation

```
     get "https://v3.football.api-sports.io/leagues?team=85&season=2019"( );

     get "https://v3.football.api-sports.io/leagues?id=61¤t=true&type=league"( );
```

Response samples

200 204 499 500

Copy Expand all Collapse all

```
     {

       "get": "leagues",

      - "parameters": {

         "id": "39"

       },

       "errors": [ ],

       "results": 1,

             "paging": {

         "current": 1,

         "total": 1

       },

      - "response": [

        + { … }

       ]

     }
```

Get the list of available seasons.

All seasons are only 4-digit keys, so for a league whose season is `2018-2019` like the English

Premier League (EPL), the `2018-2019` season in the API will be `2018` .

All  `seasons` can be used in other endpoints as filters. 

This endpoint does not require any parameters.

Update Frequency : This endpoint is updated each time a new league is added.

Recommended Calls : 1 call per day.


HEADER PARAMETERS


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 37/130


21/11/2025, 04:41 API-Football - Documentation


```
  x-apisports-key

  required

```

**200** OK

**204** No Content

**499** Time Out





**500** Internal Server Error

GET `/leagues/seasons`

Request samples

Php Python Node JavaScript Curl Ruby

```
  $client = new http Client\ ;

  $request = new http Client Request\ \ ;

```



```
$request->setRequestUrl 'https://v3.football.api-sports.io/leagues/seasons'( );

$request->setRequestMethod 'GET'( );

$request->setHeaders array( (

     'x-apisports-key' => 'XxXxXxXxXxXxXxXxXxXxXxXx'

));

$client->enqueue $request ->( ) send();

```

```
$response = $client->getResponse

```

```
();

```

```
echo $response->getBody

```

```
();

```


 

Response samples

200 204 499 500


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 38/130


21/11/2025, 04:41 API-Football - Documentation

Copy Expand all Collapse all

```
     {

       "get": "leagues/seasons",

       "parameters": [ ],

       "errors": [ ],

       "results": 12,

             "paging": {

         "current": 1,

         "total": 1

       },

      - "response": [

         2008,

         2010,

         2011,

         2012,

         2013,

         2014,

         2015,

         2016,

         2017,

         2018,

         2019,

         2020

       ]

     }

# Teams
```

Get the list of available teams.

it



The team `id` are unique in the API and teams keep it among all the leagues/cups in which they


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 39/130


21/11/2025, 04:41 API-Football - Documentation

To get the logo of a team you have to call the following url: `https://media.api-`

```
    sports.io/football/teams/{team_id}.png
```

You can find all the teams ids on our [Dashboard.](https://dashboard.api-football.com/soccer/ids/teams)

Examples available in Request samples "Use Cases".

All the parameters of this endpoint can be used together.

This endpoint requires at least one parameter.

Update Frequency : This endpoint is updated several times a week.

Recommended Calls : 1 call per day.

HOW TO GET ALL TEAMS [AND](https://www.api-football.com/tutorials/4/how-to-get-all-teams-and-players-from-a-league-id) PLAYERS FROM A LEAGUE ID

QUERY PARAMETERS


```
  id

  name

  league

  season

  country

  code

  venue

  search

```

HEADER PARAMETERS

```
  x-apisports-key

  required

```


The id of the team

The name of the team

The id of the league

integer = 4 characters YYYY

The season of the league

The country name of the team

The code of the team

The id of the venue

The name or the country name of the team



https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 40/130


21/11/2025, 04:41 API-Football - Documentation


**200** OK

**204** No Content

**499** Time Out

**500** Internal Server Error

GET `/teams`

Request samples

Use Cases Php Python Node JavaScript Curl Ruby

```
     // Get one team from one team {id}

     get "https://v3.football.api-sports.io/teams?id=33"( );

     // Get one team from one team {name}

     get "https://v3.football.api-sports.io/teams?name=manchester united"( );

     // Get all teams from one {league} & {season}

     get "https://v3.football.api-sports.io/teams?league=39&season=2019"( );

     // Get teams from one team {country}

     get "https://v3.football.api-sports.io/teams?country=england"( );

     // Get teams from one team {code}

     get "https://v3.football.api-sports.io/teams?code=FRA"( );

     // Get teams from one venue {id}

```



```
     get "https://v3.football.api-sports.io/teams?venue=789"( );

     // Allows you to search for a team in relation to a team {name} or {country}

     get "https://v3.football.api-sports.io/teams?search=manches"( );

     get "https://v3.football.api-sports.io/teams?search=England"( );
```

Response samples


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 41/130


21/11/2025, 04:41 API-Football - Documentation

200 204 499 500

Copy Expand all Collapse all

```
     {

       "get": "teams",

             "parameters": {

         "id": "33"

       },

       "errors": [ ],

       "results": 1,

             "paging": {

         "current": 1,

         "total": 1

       },

      - "response": [

        + { … }

       ]

     }
## Teams statistics
```

Returns the statistics of a team in relation to a given competition and season.

It is possible to add the `date` parameter to calculate statistics from the beginning of the season to

the given date. By default the API returns the statistics of all games played by the team for the

competition and the season.

Update Frequency : This endpoint is updated twice a day.

Recommended Calls : 1 call per day for the teams who have at least one fixture during the day

otherwise 1 call per week.

Here is an example of what can be achieved


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 42/130


21/11/2025, 04:41 API-Football - Documentation

QUERY PARAMETERS


```
  league

  required

  season

  required

  team

  required

  date

```

HEADER PARAMETERS

```
  x-apisports-key

  required

```

**200** OK

**204** No Content

**499** Time Out



The id of the league

integer = 4 characters YYYY

The season of the league

The id of the team

stringYYY ~~Y-~~ MM ~~-~~ DD

The limit date



**500** Internal Server Error


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 43/130


21/11/2025, 04:41 API-Football - Documentation

GET `/teams/statistics`

Request samples

Use Cases Php Python Node JavaScript Curl Ruby

```
     // Get all statistics for a {team} in a {league} & {season}

```



```
get "https://v3.football.api-sports.io/teams/statistics?league=39&team=33&sea(

//Get all statistics for a {team} in a {league} & {season} with a end {date}

```

```
get "https://v3.football.api-sports.io/teams/statistics?league=39&team=33&sea(

```

 



Response samples

200 204 499 500

```
  {

    "get": "teams/statistics",

      "parameters": {

      "league": "39",

      "season": "2019",

      "team": "33"

    },

    "errors": [ ],

    "results": 11,

      "paging": {

      "current": 1,

      "total": 1

    },

```


Copy Expand all Collapse all



https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 44/130


21/11/2025, 04:41 API-Football - Documentation

```
      - "response": {

        + "league": … { },

        + "team": … { },

         "form": "WDLDWLDLDWLWDDWWDLWWLWLLDWWDWDWWWWDWDW",

        + "fixtures": … { },

        + "goals": … { },

        + "biggest": … { },

        + "clean_sheet": … { },

        + "failed_to_score": … { },

        + "penalty": … { },

        + "lineups": … [ ],

        + "cards": … { }

       }

     }

## Teams seasons
```

Get the list of seasons available for a team.

Examples available in Request samples "Use Cases".

This endpoint requires at least one parameter.

Update Frequency : This endpoint is updated several times a week.

Recommended Calls : 1 call per day.

QUERY PARAMETERS


```
  team

  required

```

HEADER PARAMETERS

```
  x-apisports-key

  required

```

**200** OK



The id of the team



https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 45/130


21/11/2025, 04:41 API-Football - Documentation

**204** No Content

**499** Time Out

**500** Internal Server Error

GET `/teams/seasons`

Request samples

Use Cases Php Python Node JavaScript Curl Ruby

```
     // Get all seasons available for a team from one team {id}

```



```
     get "https://v3.football.api-sports.io/teams/seasons?team=33"( );
```

Response samples

200 204 499 500

Copy Expand all Collapse all

```
     {

       "get": "teams/seasons",

      - "parameters": {

         "team": "33"

       },

       "errors": [ ],

       "results": 1,

             "paging": {

         "current": 1,

         "total": 1

       },

```

https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 46/130


21/11/2025, 04:41 API-Football - Documentation

```
      - "response": [

         2010,

         2011,

         2012,

         2013,

         2014,

         2015,

         2016,

         2017,

         2018,

         2019,

         2020,

         2021

       ]

     }

## Teams countries
```

Get the list of countries available for the `teams` endpoint.

Update Frequency : This endpoint is updated several times a week.

Recommended Calls : 1 call per day.


HEADER PARAMETERS


```
  x-apisports-key

  required

```

**200** OK

**204** No Content

**499** Time Out





**500** Internal Server Error


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 47/130


21/11/2025, 04:41 API-Football - Documentation

GET `/teams/countries`

Request samples

Use Cases Php Python Node JavaScript Curl Ruby

```
     // Get all countries available for the teams endpoints

```



```
     get "https://v3.football.api-sports.io/teams/countries"( );
```

Response samples

200 204 499 500

Copy Expand all Collapse all

```
     {

       "get": "teams/countries",

       "parameters": [ ],

       "errors": [ ],

       "results": 258,

             "paging": {

         "current": 1,

         "total": 1

       },

      - "response": [

        + { … }

       ]

     }

# Venues

```

https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 48/130


21/11/2025, 04:41 API-Football - Documentation

## Venues

Get the list of available venues.

The venue `id` are unique in the API.

To get the image of a venue you have to call the following url: `https://media.api-`

```
    sports.io/football/venues/{venue_id}.png
```

Examples available in Request samples "Use Cases".

All the parameters of this endpoint can be used together.

This endpoint requires at least one parameter.

Update Frequency : This endpoint is updated several times a week.

Recommended Calls : 1 call per day.

QUERY PARAMETERS


```
  id

  name

  city

  country

  search

```

HEADER PARAMETERS

```
  x-apisports-key

  required

```

**200** OK



The id of the venue

The name of the venue

The city of the venue

The country name of the venue

The name, city or the country of the venue



https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 49/130


21/11/2025, 04:41 API-Football - Documentation

**204** No Content

**499** Time Out

**500** Internal Server Error

GET `/venues`

Request samples

Use Cases Php Python Node JavaScript Curl Ruby

```
     // Get one venue from venue {id}

     get "https://v3.football.api-sports.io/venues?id=556"( );

     // Get one venue from venue {name}

     get "https://v3.football.api-sports.io/venues?name=Old Trafford"( );

     // Get all venues from {city}

     get "https://v3.football.api-sports.io/venues?city=manchester"( );

     // Get venues from {country}

```



```
     get "https://v3.football.api-sports.io/venues?country=england"( );

     // Allows you to search for a venues in relation to a venue {name}, {city} or

     get "https://v3.football.api-sports.io/venues?search=trafford"( );

     get "https://v3.football.api-sports.io/venues?search=manches"( );

     get "https://v3.football.api-sports.io/venues?search=England"( );

```

 

Response samples

200 204 499 500

Copy Expand all Collapse all

```
     {

       "get": "venues",

```

https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 50/130


21/11/2025, 04:41 API-Football - Documentation

```
      - "parameters": {

         "id": "556"

       },

       "errors": [ ],

       "results": 1,

             "paging": {

         "current": 1,

         "total": 1

       },

      - "response": [

        + { … }

       ]

     }

# Standings

## Standings
```

Get the standings for a league or a team.

Return a table of one or more rankings according to the league / cup.

Some competitions have several rankings in a year, group phase, opening ranking, closing ranking etc…

Examples available in Request samples "Use Cases".

Most of the parameters of this endpoint can be used together.

Update Frequency : This endpoint is updated every hour.

Recommended Calls : 1 call per hour for the leagues or teams who have at least one fixture in progress

otherwise 1 call per day.

HOW TO GET STANDINGS [FOR](https://www.api-football.com/tutorials/6/how-to-get-standings-for-all-current-seasons) ALL CURRENT SEASONS

QUERY PARAMETERS


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 51/130


21/11/2025, 04:41 API-Football - Documentation


```
  league

  season

  required

  team

```

HEADER PARAMETERS

```
  x-apisports-key

  required

```

**200** OK

**204** No Content

**499** Time Out



The id of the league

The season of the league

The id of the team



**500** Internal Server Error

GET `/standings`

Request samples

Use Cases Php Python Node JavaScript Curl Ruby

```
  // Get all Standings from one {league} & {season}

```



```
     get "https://v3.football.api-sports.io/standings?league=39&season=2019"( );

     // Get all Standings from one {league} & {season} & {team}

     get "https://v3.football.api-sports.io/standings?league=39&team=33&season=201(

```

https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 52/130


21/11/2025, 04:41 API-Football - Documentation

```
     // Get all Standings from one {team} & {season}

     get "https://v3.football.api-sports.io/standings?team=33&season=2019"( );
```

Response samples

200 204 499 500


 

Copy Expand all Collapse all

```
     {

       "get": "standings",

      - "parameters": {

         "league": "39",

         "season": "2019"

       },

       "errors": [ ],

       "results": 1,

             "paging": {

         "current": 1,

         "total": 1

       },

      - "response": [

        + { … }

       ]

     }

# Fixtures

## Rounds
```

Get the rounds for a league or a cup.

The `round` can be used in endpoint fixtures as filters

Examples available in Request samples "Use Cases".


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 53/130


21/11/2025, 04:41 API-Football - Documentation

Update Frequency : This endpoint is updated every day.

Recommended Calls : 1 call per day.

QUERY PARAMETERS


```
  league

  required

  season

  required

  current

  dates

  timezone

```

HEADER PARAMETERS

```
  x-apisports-key

  required

```

**200** OK

**204** No Content

**499** Time Out



The id of the league

The season of the league

Enum: `"true"` `"false"`

The current round only

Default: `false`

Enum: `"true"` `"false"`

Add the dates of each round in the response

A valid timezone from the endpoint `Timezone`



**500** Internal Server Error

GET `/fixtures/rounds`


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 54/130


21/11/2025, 04:41 API-Football - Documentation

Request samples

Use Cases Php Python Node JavaScript Curl Ruby

```
     // Get all available rounds from one {league} & {season}

```



```
get "https://v3.football.api-sports.io/fixtures/rounds?league=39&season=2019"(

// Get all available rounds from one {league} & {season} With the dates of ea

```

```
get "https://v3.football.api-sports.io/fixtures/rounds?league=39&season=2019&(

// Get current round from one {league} & {season}

```

```
get "https://v3.football.api-sports.io/fixtures/rounds?league=39&season=2019&(

```

 



Response samples

200 204 499 500

```
  {

    "get": "fixtures/rounds",

  - "parameters": {

      "league": "39",

      "season": "2019"

    },

    "errors": [ ],

    "results": 38,

      "paging": {

      "current": 1,

      "total": 1

    },

```


Copy Expand all Collapse all



https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 55/130


21/11/2025, 04:41 API-Football - Documentation

```
      - "response": [

         "Regular Season - 1",

         "Regular Season - 2",

         "Regular Season - 3",

         "Regular Season - 4",

         "Regular Season - 5",

         "Regular Season - 6",

         "Regular Season - 7",

         "Regular Season - 8",

         "Regular Season - 9",

         "Regular Season - 10",

         "Regular Season - 11",

         "Regular Season - 12",

         "Regular Season - 13",

         "Regular Season - 14",

         "Regular Season - 15",

         "Regular Season - 16",

         "Regular Season - 17",

         "Regular Season - 18",

         "Regular Season - 18",

         "Regular Season - 19",

         "Regular Season - 20",

         "Regular Season - 21",

         "Regular Season - 22",

         "Regular Season - 23",

         "Regular Season - 24",

         "Regular Season - 25",

         "Regular Season - 26",

         "Regular Season - 27",

         "Regular Season - 28",

         "Regular Season - 29",

         "Regular Season - 30",

         "Regular Season - 31",

         "Regular Season - 32",

         "Regular Season - 33",

         "Regular Season - 34",

         "Regular Season - 35",

         "Regular Season - 36",

         "Regular Season - 37",

         "Regular Season - 38"

       ]

     }

```

https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 56/130


21/11/2025, 04:41 API-Football - Documentation

## Fixtures

For all requests to fixtures you can add the query parameter `timezone` to your request in order to

retrieve the list of matches in the time zone of your choice like “Europe/London“

To know the list of available time zones you have to use the endpoint timezone.

Available fixtures status















|SHORT|LONG|TYPE|DESCRIPTION|
|---|---|---|---|
|TBD|Time To Be<br>Defined|Scheduled|Scheduled but date and time are not known|
|NS|Not Started|Scheduled||
|1H|First Half, Kick<br>Off|In Play|First half in play|
|HT|Halftime|In Play|Finished in the regular time|
|2H|Second Half,<br>2nd Half<br>Started|In Play|Second half in play|
|ET|Extra Time|In Play|Extra time in play|
|BT|Break Time|In Play|Break during extra time|
|P|Penalty In<br>Progress|In Play|Penaly played after extra time|
|SUSP|Match<br>Suspended|In Play|Suspended by referee's decision, may be<br>rescheduled another day|
|INT|Match<br>Interrupted|In Play|Interrupted by referee's decision, should resume in<br>a few minutes|
|FT|Match Finished|Finished|Finished in the regular time|
|AET|Match Finished|Finished|Finished after extra time without going to the<br>penalty shootout|
|PEN|Match Finished|Finished|Finished after the penalty shootout|
|PST|Match<br>Postponed|Postponed|Postponed to another day, once the new date and<br>time is known the status will change to Not<br>Started|
|CANC|Match<br>Cancelled|Cancelled|Cancelled, match will not be played|


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 57/130


|5, 04:41|Col2|Col3|API-Football - Documentation|
|---|---|---|---|
|SHORT|LONG<br>T|YPE|DESCRIPTION|
|ABD|Match<br>Abandoned<br>A|bandoned|Abandoned for various reasons (Bad Weather,<br>Safety, Floodlights, Playing Staff Or Referees), Can<br>be rescheduled or not, it depends on the<br>competition|
|AWD|Technical Loss<br>N|ot Played||
|WO|WalkOver<br>N|ot Played|Victory by forfeit or absence of competitor|
|LIVE|In Progress<br>In|Play|Used in very rare cases. It indicates a fixture in<br>progress but the data indicating the half~~-~~time or<br>elapsed time are not available|



Fixtures with the status `TBD` may indicate an incorrect fixture date or time because the fixture date or

time is not yet known or final. Fixtures with this status are checked and updated daily. The same

applies to fixtures with the status `PST`, `CANC` .

The fixtures ids are unique and specific to each fixture. In no case an `ID` will change.

Not all competitions have livescore available and only have `final result` . In this case, the status

remains in `NS` and will be updated in the minutes/hours following the match (this can take up to 48

hours, depending on the competition).

Although the data is updated every 15 seconds, depending on the competition there may be a

delay between reality and the availability of data in the API.

Update Frequency : This endpoint is updated every 15 seconds.

Recommended Calls : 1 call per minute for the leagues, teams, fixtures who have at least one fixture in

progress otherwise 1 call per day.

Here are several examples of what can be achieved

QUERY PARAMETERS

`id` integer


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 58/130


21/11/2025, 04:41 API-Football - Documentation

Value: `"id"`

The id of the fixture


```
  ids

  live

  date

  league

  season

  team

  last

  next

  from

  to

  round

  status

  venue

  timezone

```

HEADER PARAMETERS



stringMaximum of 20 fixtures ids

Value: `"id-id-id"`

One or more fixture ids

Enum: `"all"` `"id-id"`

All or several leagues ids

stringYYY ~~Y-~~ MM ~~-~~ DD

A valid date

The id of the league

integer = 4 characters YYYY

The season of the league

The id of the team

For the X last fixtures

For the X next fixtures

stringYYY ~~Y-~~ MM ~~-~~ DD

A valid date

stringYYY ~~Y-~~ MM ~~-~~ DD

A valid date

The round of the fixture

Enum: `"NS"` `"NS-PST-FT"`

One or more fixture status short

The venue id of the fixture

A valid timezone from the endpoint `Timezone`



https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 59/130


21/11/2025, 04:41 API-Football - Documentation


```
  x-apisports-key

  required

```

**200** OK

**204** No Content

**499** Time Out





**500** Internal Server Error

GET `/fixtures`

Request samples

Use Cases Php Python Node JavaScript Curl Ruby

```
  // Get fixture from one fixture {id}

```



```
     // In this request events, lineups, statistics fixture and players fixture ar

     get "https://v3.football.api-sports.io/fixtures?id=215662"( );

     // Get fixture from severals fixtures {ids}

     // In this request events, lineups, statistics fixture and players fixture ar

     get "https://v3.football.api-sports.io/fixtures?ids=215662-215663-215664-2156(

     // Get all available fixtures in play

     // In this request events are returned in the response

     get "https://v3.football.api-sports.io/fixtures?live=all"( );

     // Get all available fixtures in play filter by several {league}

     // In this request events are returned in the response

     get "https://v3.football.api-sports.io/fixtures?live=39-61-48"( );

     // Get all available fixtures from one {league} & {season}

     get "https://v3.football.api-sports.io/fixtures?league=39&season=2019"( );

     // Get all available fixtures from one {date}

```

https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 60/130


21/11/2025, 04:41 API-Football - Documentation

```
     get "https://v3.football.api-sports.io/fixtures?date=2019-10-22"( );

     // Get next X available fixtures

     get "https://v3.football.api-sports.io/fixtures?next=15"( );

     // Get last X available fixtures

     get "https://v3.football.api-sports.io/fixtures?last=15"( );

     // It’s possible to make requests by mixing the available parameters

     get "https://v3.football.api-sports.io/fixtures?date=2020-01-30&league=61&sea(

     get "https://v3.football.api-sports.io/fixtures?league=61&next=10"( );

     get "https://v3.football.api-sports.io/fixtures?venue=358&next=10"( );

     get "https://v3.football.api-sports.io/fixtures?league=61&last=10&status=ft"( )

     get "https://v3.football.api-sports.io/fixtures?team=85&last=10&timezone=Euro(

     get "https://v3.football.api-sports.io/fixtures?team=85&season=2019&from=2019(

     get "https://v3.football.api-sports.io/fixtures?league=61&season=2019&from=20(

     get "https://v3.football.api-sports.io/fixtures?league=61&season=2019&round=R(
```

Response samples

200 204 499 500

Copy Expand all Collapse all

```
     {

       "get": "fixtures",

      - "parameters": {

         "live": "all"

       },

       "errors": [ ],

       "results": 4,

             "paging": {

         "current": 1,

```

 `"total": 1` 

```
       },

      - "response": [

        + { … }

       ]

     }

```

https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 61/130


21/11/2025, 04:41 API-Football - Documentation
## Head To Head

Get heads to heads between two teams.

Update Frequency : This endpoint is updated every 15 seconds.

Recommended Calls : 1 call per minute for the leagues, teams, fixtures who have at least one fixture in

progress otherwise 1 call per day.

Here is an example of what can be achieved

QUERY PARAMETERS


```
h2h

required

date

league

season

last

```


The ids of the teams

stringYYY ~~Y-~~ MM ~~-~~ DD

The id of the league

The season of the league

For the X last fixtures



https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 62/130


21/11/2025, 04:41 API-Football - Documentation


```
  next

  from

  to

  status

  venue

  timezone

```

HEADER PARAMETERS

```
  x-apisports-key

  required

```

**200** OK

**204** No Content

**499** Time Out



For the X next fixtures

stringYYY ~~Y-~~ MM ~~-~~ DD

stringYYY ~~Y-~~ MM ~~-~~ DD

Enum: `"NS"` `"NS-PST-FT"`

One or more fixture status short

The venue id of the fixture

A valid timezone from the endpoint `Timezone`



**500** Internal Server Error

GET `/fixtures/headtohead`

Request samples

Use Cases Php Python Node JavaScript Curl Ruby


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 63/130


21/11/2025, 04:41 API-Football - Documentation

```
     // Get all head to head between two {team}

     get "https://v3.football.api-sports.io/fixtures/headtohead?h2h=33-34"( );

     // It’s possible to make requests by mixing the available parameters

     get "https://v3.football.api-sports.io/fixtures/headtohead?h2h=33-34"( );

     get "https://v3.football.api-sports.io/fixtures/headtohead?h2h=33-34&status=n(

     get "https://v3.football.api-sports.io/fixtures/headtohead?h2h=33-34&from=201(

     get "https://v3.football.api-sports.io/fixtures/headtohead?date=2019-10-22&h2(

     get "https://v3.football.api-sports.io/fixtures/headtohead?league=39&season=2(

     get "https://v3.football.api-sports.io/fixtures/headtohead?league=39&season=2(

     get "https://v3.football.api-sports.io/fixtures/headtohead?league=39&season=2(

```

 

Response samples

200 204 499 500

Copy Expand all Collapse all

```
     {

       "get": "fixtures/headtohead",

      - "parameters": {

         "h2h": "33-34",

         "last": "1"

       },

       "errors": [ ],

       "results": 1,

             "paging": {

         "current": 1,

         "total": 1

       },

      - "response": [

        + { … }

       ]

     }
```

Get the statistics for one fixture.

Available statistics


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 64/130


21/11/2025, 04:41 API-Football - Documentation

Shots on Goal

Shots off Goal

Shots insidebox

Shots outsidebox

Total Shots

Blocked Shots

Corner Kicks

Yellow Cards

Red Cards

Total passes

Passes accurate

Update Frequency : This endpoint is updated every minute.

Recommended Calls : 1 call every minute for the teams or fixtures who have at least one fixture in

progress otherwise 1 call per day.

Here is an example of what can be achieved


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 65/130


21/11/2025, 04:41 API-Football - Documentation

QUERY PARAMETERS


```
  fixture

  required

  team

  type

  half

```

HEADER PARAMETERS



The id of the fixture

The id of the team

The type of statistics

Default: `false`

Enum: `"true"` `"false"`

Add the halftime statistics in the response `Data start from 2024`

```
season for half parameter

```


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 66/130


21/11/2025, 04:41 API-Football - Documentation


```
  x-apisports-key

  required

```

**200** OK

**204** No Content

**499** Time Out





**500** Internal Server Error

GET `/fixtures/statistics`

Request samples

Use Cases Php Python Node JavaScript Curl Ruby

```
  // Get all available statistics from one {fixture}

```



```
get "https://v3.football.api-sports.io/fixtures/statistics?fixture=215662"( );

```

```
     // Get all available statistics from one {fixture} with Fulltime, First & Sec

     get "https://v3.football.api-sports.io/fixtures/statistics?fixture=215662&hal(

     // Get all available statistics from one {fixture} & {type}

     get "https://v3.football.api-sports.io/fixtures/statistics?fixture=215662&typ(

     // Get all available statistics from one {fixture} & {team}

     get "https://v3.football.api-sports.io/fixtures/statistics?fixture=215662&tea(

```

 

Response samples

200 204 499 500


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 67/130


21/11/2025, 04:41 API-Football - Documentation

Copy Expand all Collapse all

```
     {

       "get": "fixtures/statistics",

      - "parameters": {

         "team": "463",

         "fixture": "215662"

       },

       "errors": [ ],

       "results": 1,

             "paging": {

         "current": 1,

         "total": 1

       },

      - "response": [

        + { … }

       ]

     }
```

Get the events from a fixture.

Available events

|TYPE|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
|Goal|Normal Goal|Own Goal|Penalty|Missed Penalty|
|Card|Yellow Card|Red card|||
|Subst|Substitution [1, 2, 3...]||||
|Var|Goal cancelled|Penalty confirmed|||



VARevents are available from the 202 ~~0-2~~ 021season.

Update Frequency : This endpoint is updated every 15 seconds.

Recommended Calls : 1 call per minute for the fixtures in progress otherwise 1 call per day.

You can also retrieve all the events of the fixtures in progress with to the endpoint `fixtures?`

```
    live=all
```

Here is an example of what can be achieved


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 68/130


21/11/2025, 04:41 API-Football - Documentation

QUERY PARAMETERS


```
  fixture

  required

  team

  player

  type

```

HEADER PARAMETERS

```
  x-apisports-key

  required

```

**200** OK

**204** No Content

**499** Time Out



The id of the fixture

The id of the team

The id of the player

The type



**500** Internal Server Error

GET `/fixtures/events`

Request samples


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 69/130


21/11/2025, 04:41 API-Football - Documentation

Use Cases Php Python Node JavaScript Curl Ruby

```
     // Get all available events from one {fixture}

```



```
     get "https://v3.football.api-sports.io/fixtures/events?fixture=215662"( );

     // Get all available events from one {fixture} & {team}

     get "https://v3.football.api-sports.io/fixtures/events?fixture=215662&team=46(

     // Get all available events from one {fixture} & {player}

     get "https://v3.football.api-sports.io/fixtures/events?fixture=215662&player=(

     // Get all available events from one {fixture} & {type}

     get "https://v3.football.api-sports.io/fixtures/events?fixture=215662&type=ca(

     // It’s possible to make requests by mixing the available parameters

     get "https://v3.football.api-sports.io/fixtures/events?fixture=215662&player=(

     get "https://v3.football.api-sports.io/fixtures/events?fixture=215662&team=46(

```

 

Response samples

200 204 499 500

Copy Expand all Collapse all

```
     {

       "get": "fixtures/events",

      - "parameters": {

         "fixture": "215662"

       },

       "errors": [ ],

       "results": 18,

             "paging": {

         "current": 1,

         "total": 1

       },

```

https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 70/130


21/11/2025, 04:41 API-Football - Documentation

```
      - "response": [

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { … }

       ]

     }

## Lineups
```

Get the lineups for a fixture.

Lineups are available between 20 and 40 minutes before the fixture when the competition covers this

feature. You can check this with the endpoint `leagues` and the `coverage` field.

It's possible that for some competitions the lineups are not available before the fixture, in this

case, they are updated and available after the match with a variable delay depending on the

Available datas

Start XI

Players' positions on the grid `*`

X = row and Y = column (X:Y)


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 71/130


21/11/2025, 04:41 API-Football - Documentation

Line 1 X being the one of the goal and then for each line this number is incremented. The column Y will

go from left to right, and incremented for each player of the line.

```
    * As a new feature, some irregularities may occur, do not hesitate to report them

    on our public Roadmap
```

Update Frequency : This endpoint is updated every 15 minutes.

Recommended Calls : 1 call every 15 minutes for the fixtures in progress otherwise 1 call per day.

Here are several examples of what can be done

QUERY PARAMETERS


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 72/130


21/11/2025, 04:41 API-Football - Documentation


```
  fixture

  required

  team

  player

  type

```

HEADER PARAMETERS

```
  x-apisports-key

  required

```

**200** OK

**204** No Content

**499** Time Out



The id of the fixture

The id of the team

The id of the player

The type



**500** Internal Server Error

GET `/fixtures/lineups`

Request samples

Use Cases Php Python Node JavaScript Curl Ruby

```
  // Get all available lineups from one {fixture}

```



```
     get "https://v3.football.api-sports.io/fixtures/lineups?fixture=592872"( );

     // Get all available lineups from one {fixture} & {team}

     get "https://v3.football.api-sports.io/fixtures/lineups?fixture=592872&team=5(

```

https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 73/130


21/11/2025, 04:41 API-Football - Documentation

```
     // Get all available lineups from one {fixture} & {player}

     get "https://v3.football.api-sports.io/fixtures/lineups?fixture=215662&player(

     // Get all available lineups from one {fixture} & {type}

     get "https://v3.football.api-sports.io/fixtures/lineups?fixture=215662&type=s(

     // It’s possible to make requests by mixing the available parameters

     get "https://v3.football.api-sports.io/fixtures/lineups?fixture=215662&player(

     get "https://v3.football.api-sports.io/fixtures/lineups?fixture=215662&team=4(
```

Response samples

200 204 499 500


 Content type 

Copy Expand all Collapse all

```
     {

       "get": "fixtures/lineups",

      - "parameters": {

         "fixture": "592872"

       },

       "errors": [ ],

       "results": 2,

             "paging": {

         "current": 1,

         "total": 1

       },

      - "response": [

        + { …,}

        + { … }

       ]

     }
## Players statistics
```

Get the players statistics from one fixture.

Update Frequency : This endpoint is updated every minute.

Recommended Calls : 1 call every minute for the fixtures in progress otherwise 1 call per day.


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 74/130


21/11/2025, 04:41 API-Football - Documentation

QUERY PARAMETERS


```
  fixture

  required

  team

```

HEADER PARAMETERS

```
  x-apisports-key

  required

```

**200** OK

**204** No Content

**499** Time Out



The id of the fixture

The id of the team



**500** Internal Server Error

GET `/fixtures/players`

Request samples

Use Cases Php Python Node JavaScript Curl Ruby

```
  // Get all available players statistics from one {fixture}

```



```
     get "https://v3.football.api-sports.io/fixtures/players?fixture=169080"( );

     // Get all available players statistics from one {fixture} & {team}

     get "https://v3.football.api-sports.io/fixtures/players?fixture=169080&team=2(

```

 

Response samples


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 75/130


21/11/2025, 04:41 API-Football - Documentation

200 204 499 500

Copy Expand all Collapse all

```
     {

       "get": "fixtures/players",

             "parameters": {

         "fixture": "169080"

       },

       "errors": [ ],

       "results": 2,

             "paging": {

         "current": 1,

         "total": 1

       },

      - "response": [

        + { … }

       ]

     }

# Injuries

## Injuries
```

Get the list of players not participating in the fixtures for various reasons such as `suspended`,

Being a new endpoint, the data is only available from April 2021.

There are two types:

`Missing Fixture` : The player will not play the fixture.

`Questionable` : The information is not yet 100% sure, the player may eventually play the fixture.

Examples available in Request samples "Use Cases".

All the parameters of this endpoint can be used together.


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 76/130


21/11/2025, 04:41 API-Football - Documentation

This endpoint requires at least one parameter.

Update Frequency : This endpoint is updated every 4 hours.

Recommended Calls : 1 call per day.

QUERY PARAMETERS


```
  league

  season

  fixture

  team

  player

  date

  ids

  timezone

```

HEADER PARAMETERS

```
  x-apisports-key

  required

```

**200** OK

**204** No Content



The id of the league

The season of the league, required with `league`, `team` and `player`

The id of the fixture

The id of the team

The id of the player

stringYYY ~~Y-~~ MM ~~-~~ DD

A valid date

stringMaximum of 20 fixtures ids

Value: `"id-id-id"`

One or more fixture ids

A valid timezone from the endpoint `Timezone`



https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 77/130


21/11/2025, 04:41 API-Football - Documentation

**499** Time Out

**500** Internal Server Error

GET `/injuries`

Request samples

Use Cases Php Python Node JavaScript Curl Ruby

```
     // Get all available injuries from one {league} & {season}

     get "https://v3.football.api-sports.io/injuries?league=2&season=2020"( );

     // Get all available injuries from one {fixture}

     get "https://v3.football.api-sports.io/injuries?fixture=686314"( );

     // Get all available injuries from severals fixtures {ids}

```



```
     get "https://v3.football.api-sports.io/injuries?ids=686314-686315-686316-6863(

     // Get all available injuries from one {team} & {season}

     get "https://v3.football.api-sports.io/injuries?team=85&season=2020"( );

     // Get all available injuries from one {player} & {season}

     get "https://v3.football.api-sports.io/injuries?player=865&season=2020"( );

     // Get all available injuries from one {date}

     get "https://v3.football.api-sports.io/injuries?date=2021-04-07"( );

     // It’s possible to make requests by mixing the available parameters

     get "https://v3.football.api-sports.io/injuries?league=2&season=2020&team=85"(

     get "https://v3.football.api-sports.io/injuries?league=2&season=2020&player=8(

     get "https://v3.football.api-sports.io/injuries?date=2021-04-07&timezone=Euro(

     get "https://v3.football.api-sports.io/injuries?date=2021-04-07&league=61"( );

```

 

Response samples

200 204 499 500


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 78/130


21/11/2025, 04:41 API-Football - Documentation

Copy Expand all Collapse all

```
     {

       "get": "injuries",

      - "parameters": {

         "fixture": "686314"

       },

       "errors": [ ],

       "results": 13,

             "paging": {

         "current": 1,

         "total": 1

       },

      - "response": [

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { … }

       ]

     }

# Predictions

## Predictions
```

Get predictions about a fixture.

The predictions are made using several algorithms including the poisson distribution, comparison of

team statistics, last matches, players etc…


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 79/130


21/11/2025, 04:41 API-Football - Documentation

Bookmakers odds are not used to make these predictions

Also provides some comparative statistics between teams

Available Predictions

Match winner : Id of the team that can potentially win the fixture

Win or Draw : If `True` indicates that the designated team can win or draw

Under / Over : ~~-~~ 1.5 / ~~-~~ 2.5 / ~~-~~ 3.5 / ~~-~~ 4.5 / +1.5 / +2.5 / +3.5 / +4.5 `*`

Goals Home : ~~-~~ 1.5 / ~~-~~ 2.5 / ~~-~~ 3.5 / ~~-~~ 4.5 `*`

Goals Away ~~-~~ 1.5 / ~~-~~ 2.5 / ~~-~~ 3.5 / ~~-~~ 4.5 `*`

Advice (Ex : Deportivo Santanior draws and ~~-3~~ .5goals)

`*` -1.5 means that there will be a maximum of 1.5 goals in the fixture, i.e : 1 goal

Update Frequency : This endpoint is updated every hour.

Recommended Calls : 1 call per hour for the fixtures in progress otherwise 1 call per day.

Here is an example of what can be achieved

QUERY PARAMETERS


```
  fixture

  required

```

HEADER PARAMETERS

```
  x-apisports-key

  required

```


The id of the fixture



https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 80/130


21/11/2025, 04:41 API-Football - Documentation


**200** OK

**204** No Content

**499** Time Out

**500** Internal Server Error

GET `/predictions`

Request samples

Use Cases Php Python Node JavaScript Curl Ruby

```
     // Get all available predictions from one {fixture}

```



```
     get "https://v3.football.api-sports.io/predictions?fixture=198772"( );
```

Response samples

200 204 499 500

Copy Expand all Collapse all


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 81/130


21/11/2025, 04:41 API-Football - Documentation

```
     {

       "get": "predictions",

      - "parameters": {

         "fixture": "198772"

       },

       "errors": [ ],

       "results": 1,

             "paging": {

         "current": 1,

         "total": 1

       },

      - "response": [

        + { … }

       ]

     }
```

Get all the information about the coachs and their careers.

To get the photo of a coach you have to call the following url: `https://media.api-`

```
    sports.io/football/coachs/{coach_id}.png
```

Update Frequency : This endpoint is updated every day.

Recommended Calls : 1 call per day.

QUERY PARAMETERS


```
id

team

```


The id of the coach

The id of the team



https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 82/130


21/11/2025, 04:41 API-Football - Documentation


```
  search

```

HEADER PARAMETERS

```
  x-apisports-key

  required

```

**200** OK

**204** No Content

**499** Time Out



The name of the coach



**500** Internal Server Error

GET `/coachs`

Request samples

Use Cases Php Python Node JavaScript Curl Ruby

```
  // Get coachs from one coach {id}

```



```
     get "https://v3.football.api-sports.io/coachs?id=1"( );

     // Get coachs from one {team}

     get "https://v3.football.api-sports.io/coachs?team=33"( );

     // Allows you to search for a coach in relation to a coach {name}

     get "https://v3.football.api-sports.io/coachs?search=Klopp"( );
```

Response samples

200 204 499 500


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 83/130


21/11/2025, 04:41 API-Football - Documentation

Copy Expand all Collapse all

```
     {

       "get": "coachs",

      - "parameters": {

         "team": "85"

       },

       "errors": [ ],

       "results": 1,

             "paging": {

         "current": 1,

         "total": 1

       },

      - "response": [

        + { … }

       ]

     }

# Players
```

Get all available seasons for players statistics.

Update Frequency : This endpoint is updated every day.

Recommended Calls : 1 call per day.

QUERY PARAMETERS


```
  player

```

HEADER PARAMETERS



The id of the player



https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 84/130


21/11/2025, 04:41 API-Football - Documentation


```
  x-apisports-key

  required

```

**200** OK

**204** No Content

**499** Time Out





**500** Internal Server Error

GET `/players/seasons`

Request samples

Use Cases Php Python Node JavaScript Curl Ruby

```
  // Get all seasons available for players endpoint

```



```
     get "https://v3.football.api-sports.io/players/seasons"( );

     // Get all seasons available for a player {id}

     get "https://v3.football.api-sports.io/players/seasons?player=276"( );
```

Response samples

200 204 499 500

Copy Expand all Collapse all

```
     {

       "get": "players/seasons",

       "parameters": [ ],

       "errors": [ ],

       "results": 35,

```

https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 85/130


21/11/2025, 04:41 API-Football - Documentation

```
             "paging": {

         "current": 1,

         "total": 1

       },

      - "response": [

         1966,

         1982,

         1986,

         1990,

         1991,

         1992,

         1993,

         1994,

         1995,

         1996,

         1997,

         1998,

         1999,

         2000,

         2001,

         2002,

         2003,

         2004,

         2005,

         2006,

         2007,

         2008,

         2009,

         2010,

         2011,

         2012,

         2013,

         2014,

         2015,

         2016,

         2017,

         2018,

         2019,

         2020,

         2022

       ]

     }

```

https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 86/130


21/11/2025, 04:41 API-Football - Documentation

Returns the list of all available players.

It is possible to call this endpoint without parameters, but you will need to use the pagination to get all

available players.

To get the photo of a player you have to call the following url: `https://media.api-`

```
    sports.io/football/players/{player_id}.png
```

This endpoint uses a pagination system, you can navigate between the different pages with to the

`page` parameter.

Pagination : 250 results per page.

Update Frequency : This endpoint is updated several times a week.

Recommended Calls : 1 call per week.

QUERY PARAMETERS


```
  player

  search

  page

```

HEADER PARAMETERS

```
  x-apisports-key

  required

```

**200** OK

**204** No Content

**499** Time Out



The id of the player

The lastname of the player

Use for the pagination



https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 87/130


21/11/2025, 04:41 API-Football - Documentation

**500** Internal Server Error

GET `/players/profiles`

Request samples

Use Cases Php Python Node JavaScript Curl Ruby

```
     // Get data from one {player}

     get "https://v3.football.api-sports.io/players/profiles?player=276"( );

     // Allows you to search for a player in relation to a player {lastname}

```



```
     get "https://v3.football.api-sports.io/players/profiles?search=ney"( );

     // Get all available Players (limited to 250 results, use the pagination for

     get "https://v3.football.api-sports.io/players/profiles"( );

     get "https://v3.football.api-sports.io/players/profiles?page=2"( );

     get "https://v3.football.api-sports.io/players/profiles?page=3"( );

```

 

Response samples

200 204 499 500

Copy Expand all Collapse all

```
     {

       "get": "players/profiles",

      - "parameters": {

         "player": "276"

       },

       "errors": [ ],

       "results": 1,

             "paging": {

         "current": 1,

         "total": 1

       },

```

https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 88/130


21/11/2025, 04:41 API-Football - Documentation

```
      - "response": [

        + { … }

       ]

     }
```

Get players statistics.

This endpoint returns the players for whom the `profile` and `statistics` data are available. Note

it



that it is possible that a player has statistics for 2 teams in the same season in case of transfers.

The statistics are calculated according to the team `id`, league `id` and `season` .

You can find the available `seasons` by using the endpoint `players/seasons` .

it



To get the squads of the teams it is better to use the endpoint `players/squads` .

it



The players `id` are unique in the API and players keep it among all the teams they have been in.

In this endpoint you have the `rating` field, which is the rating of the player according to a match or a

season. This data is calculated according to the performance of the player in relation to the other
players of the game or the season who occupy the same position (Attacker, defender, goal...). There are

different algorithms that take into account the position of the player and assign points according to his

To get the photo of a player you have to call the following url: `https://media.api-`

```
    sports.io/football/players/{player_id}.png
```

This endpoint uses a pagination system, you can navigate between the different pages with to the

`page` parameter.

Pagination : 20 results per page.

Update Frequency : This endpoint is updated several times a week.

Recommended Calls : 1 call per day.

HOW TO GET ALL TEAMS [AND](https://www.api-football.com/tutorials/4/how-to-get-all-teams-and-players-from-a-league-id) PLAYERS FROM A LEAGUE ID

QUERY PARAMETERS


```
id

team

```


The id of the player



https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 89/130


21/11/2025, 04:41 API-Football - Documentation

The id of the team


```
  league

  season

  search

  page

```

HEADER PARAMETERS

```
  x-apisports-key

  required

```

**200** OK

**204** No Content

**499** Time Out



The id of the league

integer = 4 characters YYYY | Requires the fields Id, League or Team...

The season of the league

string >= 4 characters Requires the fields League or Team

The name of the player

Use for the pagination



**500** Internal Server Error

GET `/players`

Request samples

Use Cases Php Python Node JavaScript Curl Ruby

```
  // Get all players statistics from one player {id} & {season}

```



```
     get "https://v3.football.api-sports.io/players?id=19088&season=2018"( );

     // Get all players statistics from one {team} & {season}

```

https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 90/130


21/11/2025, 04:41 API-Football - Documentation

```
     get "https://v3.football.api-sports.io/players?season=2018&team=33"( );

     get "https://v3.football.api-sports.io/players?season=2018&team=33&page=2"( );

     // Get all players statistics from one {league} & {season}

     get "https://v3.football.api-sports.io/players?season=2018&league=61"( );

     get "https://v3.football.api-sports.io/players?season=2018&league=61&page=4"( )

     // Get all players statistics from one {league}, {team} & {season}

     get "https://v3.football.api-sports.io/players?season=2018&league=61&team=33"(

     get "https://v3.football.api-sports.io/players?season=2018&league=61&team=33&(

     // Allows you to search for a player in relation to a player {name}

     get "https://v3.football.api-sports.io/players?team=85&search=cavani"( );

     get "https://v3.football.api-sports.io/players?league=61&search=cavani"( );

     get "https://v3.football.api-sports.io/players?team=85&search=cavani&season=2(
```

Response samples

Copy Expand all Collapse all

```
     {

       "get": "players",

      - "parameters": {

         "id": "276",

         "season": "2019"

       },

       "errors": [ ],

       "results": 1,

             "paging": {

         "current": 1,

         "total": 1

       },

      - "response": [

        + { … }

       ]

     }

## Squads

```

https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 91/130


21/11/2025, 04:41 API-Football - Documentation

Return the current squad of a team when the `team` parameter is used. When the `player` parameter

is used the endpoint returns the set of teams associated with the player.

The response format is the same regardless of the parameter sent.

This endpoint requires at least one parameter.

Update Frequency : This endpoint is updated several times a week.

Recommended Calls : 1 call per week.

QUERY PARAMETERS


```
  team

  player

```

HEADER PARAMETERS

```
  x-apisports-key

  required

```

**200** OK

**204** No Content

**499** Time Out



The id of the team

The id of the player



**500** Internal Server Error

GET `/players/squads`

Request samples

Use Cases Php Python Node JavaScript Curl Ruby


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 92/130


21/11/2025, 04:41 API-Football - Documentation

```
     // Get all players from one {team}

     get "https://v3.football.api-sports.io/players/squads?team=33"( );

     // Get all teams from one {player}

     get "https://v3.football.api-sports.io/players/squads?player=276"( );
```

Response samples

200 204 499 500

Copy Expand all Collapse all

```
     {

       "get": "players/squads",

             "parameters": {

         "team": "33"

       },

       "errors": [ ],

       "results": 1,

             "paging": {

         "current": 1,

         "total": 1

       },

      - "response": [

        + { … }

       ]

     }

## Teams
```

Returns the list of teams and seasons in which the player played during his career.

This endpoint requires at least one parameter.

Update Frequency : This endpoint is updated several times a week.

Recommended Calls : 1 call per week.

QUERY PARAMETERS


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 93/130


21/11/2025, 04:41 API-Football - Documentation


```
  player

  required

```

HEADER PARAMETERS

```
  x-apisports-key

  required

```

**200** OK

**204** No Content

**499** Time Out



The id of the player



**500** Internal Server Error

GET `/players/teams`

Request samples

Use Cases Php Python Node JavaScript Curl Ruby

```
  // Get all teams from one {player}

```



```
     get "https://v3.football.api-sports.io/players/teams?player=276"( );
```

Response samples

200 204 499 500

Copy Expand all Collapse all

```
     {

       "get": "players/teams",

```

https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 94/130


21/11/2025, 04:41 API-Football - Documentation

```
      - "parameters": {

         "player": "276"

       },

       "errors": [ ],

       "results": 8,

             "paging": {

         "current": 1,

         "total": 1

       },

      - "response": [

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { … }

       ]

     }
## Top Scorers
```

Get the 20 best players for a league or cup.

How it is calculated:

1 : The player that has scored the higher number of goals

2 : The player that has scored the fewer number of penalties

3 : The player that has delivered the higher number of goal assists

4 : The player that scored their goals in the higher number of matches

5 : The player that played the fewer minutes

6 : The player that plays for the team placed higher on the table

7 : The player that received the fewer number of red cards

8 : The player that received the fewer number of yellow cards

Update Frequency : This endpoint is updated several times a week.

Recommended Calls : 1 call per day.

QUERY PARAMETERS


```
league

required

```


The id of the league



https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 95/130


21/11/2025, 04:41 API-Football - Documentation


```
  season

  required

```

HEADER PARAMETERS

```
  x-apisports-key

  required

```

**200** OK

**204** No Content

**499** Time Out



integer = 4 characters YYYY

The season of the league



**500** Internal Server Error

GET `/players/topscorers`

Request samples

Php Python Node JavaScript Curl Ruby

```
  $client = new http Client\ ;

  $request = new http Client Request\ \ ;

```



```
$request->setRequestUrl 'https://v3.football.api-sports.io/players/topscorers(

$request->setRequestMethod 'GET'( );

$request->setQuery new( http QueryString\ array( (

```

```
'season' => '2018',

'league' => '61'

```

```
     )));

     $request->setHeaders array( (

          'x-apisports-key' => 'XxXxXxXxXxXxXxXxXxXxXxXx'

     ));

     $client->enqueue $request ->( ) send();

```

https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 96/130


21/11/2025, 04:41 API-Football - Documentation


```
$response = $client->getResponse

```

```
();

```

```
  echo $response->getBody
```

Response samples


```
();

```


200 204 499 500

```
{

  "get": "players/topscorers",

 - "parameters": {

    "league": "61",

```


Copy Expand all Collapse all



 `"season": "2018"` 

```
       },

       "errors": [ ],

       "results": 20,

             "paging": {

         "current": 1,

         "total": 1

       },

      - "response": [

        + { …,}

        + { … }

       ]

     }
## Top Assists
```

Get the 20 best players assists for a league or cup.

How it is calculated:

1 : The player that has delivered the higher number of goal assists

2 : The player that has scored the higher number of goals

3 : The player that has scored the fewer number of penalties

4 : The player that assists in the higher number of matches

5 : The player that played the fewer minutes

6 : The player that received the fewer number of red cards

7 : The player that received the fewer number of yellow cards


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 97/130


21/11/2025, 04:41 API-Football - Documentation

Update Frequency : This endpoint is updated several times a week.

Recommended Calls : 1 call per day.

QUERY PARAMETERS


```
  league

  required

  season

  required

```

HEADER PARAMETERS

```
  x-apisports-key

  required

```

**200** OK

**204** No Content

**499** Time Out



The id of the league

The season of the league



**500** Internal Server Error

GET `/players/topassists`

Request samples

Php Python Node JavaScript Curl Ruby

```
     $client = new http Client\ ;

     $request = new http Client Request\ \ ;

     $request->setRequestUrl 'https://v3.football.api-sports.io/players/topassists(

     $request->setRequestMethod 'GET'( );

     $request->setQuery new( http QueryString\ array( (

```

https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 98/130


21/11/2025, 04:41 API-Football - Documentation


```
'season' => '2020',

'league' => '61'

```

```
)));

$request->setHeaders array( (

     'x-apisports-key' => 'XxXxXxXxXxXxXxXxXxXxXxXx'

));

$client->enqueue $request ->( ) send();

```

```
$response = $client->getResponse

```

```
();

```

```
  echo $response->getBody
```

Response samples


```
();

```


200 204 499 500


 

Content type

Copy Expand all Collapse all

```
     {

       "get": "players/topassists",

      - "parameters": {

         "season": "2020",

         "league": "61"

       },

       "errors": [ ],

       "results": 20,

             "paging": {

         "current": 0,

         "total": 1

       },

```

https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 99/130


21/11/2025, 04:41 API-Football - Documentation

```
      - "response": [

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { … }

       ]

     }
## Top Yellow Cards
```

Get the 20 players with the most yellow cards for a league or cup.

How it is calculated:

1 : The player that received the higher number of yellow cards

2 : The player that received the higher number of red cards

3 : The player that assists in the higher number of matches

4 : The player that played the fewer minutes

Update Frequency : This endpoint is updated several times a week.

Recommended Calls : 1 call per day.

QUERY PARAMETERS


```
league

required

```


The id of the league



https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 100/130


21/11/2025, 04:41 API-Football - Documentation


```
  season

  required

```

HEADER PARAMETERS

```
  x-apisports-key

  required

```

**200** OK

**204** No Content

**499** Time Out



integer = 4 characters YYYY

The season of the league



**500** Internal Server Error

GET `/players/topyellowcards`

Request samples

Php Python Node JavaScript Curl Ruby

```
  $client = new http Client\ ;

  $request = new http Client Request\ \ ;

```



```
$request->setRequestUrl 'https://v3.football.api-sports.io/players/topyellowc(

$request->setRequestMethod 'GET'( );

$request->setQuery new( http QueryString\ array( (

```

```
'season' => '2020',

'league' => '61'

```

```
     )));

     $request->setHeaders array( (

          'x-apisports-key' => 'XxXxXxXxXxXxXxXxXxXxXxXx'

     ));

     $client->enqueue $request ->( ) send();

```

https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 101/130


21/11/2025, 04:41 API-Football - Documentation


```
$response = $client->getResponse

```

```
();

```

```
  echo $response->getBody
```

Response samples


```
();

```


200 204 499 500

```
{

  "get": "players/topyellowcards",

 - "parameters": {

    "season": "2020",

```


Copy Expand all Collapse all



 `"league": "61"` 

```
       },

       "errors": [ ],

       "results": 20,

             "paging": {

         "current": 0,

         "total": 1

       },

```

https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 102/130


21/11/2025, 04:41 API-Football - Documentation

```
      - "response": [

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { … }

       ]

     }
## Top Red Cards
```

Get the 20 players with the most red cards for a league or cup.

How it is calculated:

1 : The player that received the higher number of red cards

2 : The player that received the higher number of yellow cards

3 : The player that assists in the higher number of matches

4 : The player that played the fewer minutes

Update Frequency : This endpoint is updated several times a week.

Recommended Calls : 1 call per day.

QUERY PARAMETERS


```
league

required

```


The id of the league



https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 103/130


21/11/2025, 04:41 API-Football - Documentation


```
  season

  required

```

HEADER PARAMETERS

```
  x-apisports-key

  required

```

**200** OK

**204** No Content

**499** Time Out



integer = 4 characters YYYY

The season of the league



**500** Internal Server Error

GET `/players/topredcards`

Request samples

Php Python Node JavaScript Curl Ruby

```
  $client = new http Client\ ;

  $request = new http Client Request\ \ ;

```



```
$request->setRequestUrl 'https://v3.football.api-sports.io/players/topredcard(

$request->setRequestMethod 'GET'( );

$request->setQuery new( http QueryString\ array( (

```

```
'season' => '2020',

'league' => '61'

```

```
     )));

     $request->setHeaders array( (

          'x-apisports-key' => 'XxXxXxXxXxXxXxXxXxXxXxXx'

     ));

     $client->enqueue $request ->( ) send();

```

https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 104/130


21/11/2025, 04:41 API-Football - Documentation


```
$response = $client->getResponse

```

```
();

```

```
  echo $response->getBody
```

Response samples


```
();

```


200 204 499 500

```
{

  "get": "players/topredcards",

 - "parameters": {

    "season": "2020",

```


Copy Expand all Collapse all



 `"league": "61"` 

```
       },

       "errors": [ ],

       "results": 20,

             "paging": {

         "current": 0,

         "total": 1

       },

```

https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 105/130


21/11/2025, 04:41 API-Football - Documentation

```
      - "response": [

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { … }

       ]

     }
```

Get all available transfers for players and teams

Update Frequency : This endpoint is updated several times a week.

Recommended Calls : 1 call per day.

QUERY PARAMETERS


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 106/130


21/11/2025, 04:41 API-Football - Documentation


```
  player

  team

```

HEADER PARAMETERS

```
  x-apisports-key

  required

```

**200** OK

**204** No Content

**499** Time Out



The id of the player

The id of the team



**500** Internal Server Error

GET `/transfers`

Request samples

Use Cases Php Python Node JavaScript Curl Ruby

```
  // Get all transfers from one {player}

```



```
     get "https://v3.football.api-sports.io/transfers?player=35845"( );

     // Get all transfers from one {team}

     get "https://v3.football.api-sports.io/transfers?team=463"( );
```

Response samples

200 204 499 500


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 107/130


21/11/2025, 04:41 API-Football - Documentation

Copy Expand all Collapse all

```
     {

       "get": "transfers",

      - "parameters": {

         "player": "35845"

       },

       "errors": [ ],

       "results": 1,

             "paging": {

         "current": 1,

         "total": 1

       },

      - "response": [

        + { … }

       ]

     }
```

Get all available trophies for a player or a coach.

Update Frequency : This endpoint is updated several times a week.

Recommended Calls : 1 call per day.

QUERY PARAMETERS


```
player

```


The id of the player



https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 108/130


21/11/2025, 04:41 API-Football - Documentation


```
  players

  coach

  coachs

```

HEADER PARAMETERS

```
  x-apisports-key

  required

```

**200** OK

**204** No Content

**499** Time Out



stringMaximum of 20 players ids

Value: `"id-id-id"`

One or more players ids

The id of the coach

stringMaximum of 20 coachs ids

Value: `"id-id-id"`

One or more coachs ids



**500** Internal Server Error

GET `/trophies`

Request samples

Use Cases Php Python Node JavaScript Curl Ruby

```
  // Get all trophies from one {player}

```



```
     get "https://v3.football.api-sports.io/trophies?player=276"( );

     // Get all trophies from several {player} ids

     get "https://v3.football.api-sports.io/trophies?players=276-278"( );

     // Get all trophies from one {coach}

```

https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 109/130


21/11/2025, 04:41 API-Football - Documentation

```
     get "https://v3.football.api-sports.io/trophies?coach=2"( );

     // Get all trophies from several {coach} ids

     get "https://v3.football.api-sports.io/trophies?coachs=2-6"( );
```

Response samples

200 204 499 500

Copy Expand all Collapse all

```
     {

       "get": "trophies",

             "parameters": {

         "player": "276"

       },

       "errors": [ ],

       "results": 38,

             "paging": {

         "current": 1,

         "total": 1

       },

      - "response": [

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { … }

       ]

     }

```

https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 110/130


21/11/2025, 04:41 API-Football - Documentation

# Sidelined

## Sidelined

Get all available sidelined for a player or a coach.

Update Frequency : This endpoint is updated several times a week.

Recommended Calls : 1 call per day.

QUERY PARAMETERS


```
  player

  players

  coach

  coachs

```

HEADER PARAMETERS

```
  x-apisports-key

  required

```

**200** OK

**204** No Content

**499** Time Out



The id of the player

stringMaximum of 20 players ids

Value: `"id-id-id"`

One or more players ids

The id of the coach

stringMaximum of 20 coachs ids

Value: `"id-id-id"`

One or more coachs ids



https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 111/130


21/11/2025, 04:41 API-Football - Documentation

**500** Internal Server Error

GET `/sidelined`

Request samples

Use Cases Php Python Node JavaScript Curl Ruby

```
     // Get all from one {player}

     get "https://v3.football.api-sports.io/sidelined?player=276"( );

     // Get all from several {player} ids

```



```
     get "https://v3.football.api-sports.io/sidelined?players=276-278-279-280-281-(

     // Get all from one {coach}

     get "https://v3.football.api-sports.io/sidelined?coach=2"( );

     // Get all from several {coach} ids

     get "https://v3.football.api-sports.io/sidelined?coachs=2-6-44-77-54-52"( );

```

 

Response samples

200 204 499 500

Copy Expand all Collapse all

```
     {

       "get": "sidelined",

      - "parameters": {

         "player": "276"

       },

       "errors": [ ],

       "results": 27,

```

https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 112/130


21/11/2025, 04:41 API-Football - Documentation

```
             "paging": {

         "current": 1,

         "total": 1

       },

      - "response": [

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { … }

       ]

     }
# Odds (In-Play)

```

https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 113/130


21/11/2025, 04:41 API-Football - Documentation

This endpoint returns in ~~-~~ play odds for fixtures in progress.

Fixtures are added between 15 and 5 minutes before the start of the fixture. Once the fixture is over

they are removed from the endpoint between 5 and 20 minutes. No history is stored. So fixtures that

are about to start, fixtures in progress and fixtures that have just ended are available in this endpoint.

Update Frequency : This endpoint is updated every 5 seconds. `*`

```
    * This value can change in the range of 5 to 60 seconds
```

INFORMATIONS ABOUT STATUS











INFORMATIONS ABOUT VALUES

When several identical values exist for the same bet the `main` field is set to `True` for the bet being

considered, the others will have the value `False` .

The `main` field will be set to `True` only if several identical values exist for the same bet.

When a value is unique for a bet the `main` value will always be `False` or `null` .

Example below :











QUERY PARAMETERS


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 114/130


21/11/2025, 04:41 API-Football - Documentation


```
  fixture

  league

  bet

```

HEADER PARAMETERS

```
  x-apisports-key

  required

```

**200** OK

**204** No Content

**499** Time Out



The id of the fixture

integer (In this endpoint the "season" parameter is ... Show pattern

The id of the league

The id of the bet



**500** Internal Server Error

GET `/odds/live`

Request samples

Use Cases Php Python Node JavaScript Curl Ruby

```
  // Get all available odds

```



```
     get "https://v3.football.api-sports.io/odds/live"( );

     // Get all available odds from one {fixture}

     get "https://v3.football.api-sports.io/odds/live?fixture=164327"( );

     // Get all available odds from one {league}

     get "https://v3.football.api-sports.io/odds/live?league=39"( );

```

https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 115/130


21/11/2025, 04:41 API-Football - Documentation

```
     // It’s possible to make requests by mixing the available parameters

     get "https://v3.football.api-sports.io/odds/live?bet=4&league=39"( );

     get "https://v3.football.api-sports.io/odds/live?bet=4&fixture=164327"( );
```

Response samples

200 204 499 500

Copy Expand all Collapse all

```
     {

       "get": "odds/live",

      - "parameters": {

         "fixture": "721238"

       },

       "errors": [ ],

       "results": 1,

             "paging": {

         "current": 1,

         "total": 1

       },

      - "response": [

        + { … }

       ]

     }

## odds/live/bets
```

Get all available bets for in ~~-~~ play odds.

All bets `id` can be used in endpoint `odds/live` as filters, but are not compatible with endpoint

`odds` for pre-match odds.

Update Frequency : This endpoint is updated every 60 seconds.

QUERY PARAMETERS


```
id

```


The id of the bet name



https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 116/130


21/11/2025, 04:41 API-Football - Documentation


```
  search

```

HEADER PARAMETERS

```
  x-apisports-key

  required

```

**200** OK

**204** No Content

**499** Time Out



The name of the bet



**500** Internal Server Error

GET `/odds/live/bets`

Request samples

Use Cases Php Python Node JavaScript Curl Ruby

```
  // Get all available bets

```



```
     get "https://v3.football.api-sports.io/odds/live/bets"( );

     // Get bet from one {id}

     get "https://v3.football.api-sports.io/odds/live/bets?id=1"( );

     // Allows you to search for a bet in relation to a bets {name}

     get "https://v3.football.api-sports.io/odds/live/bets?search=winner"( );
```

Response samples

200 204 499 500


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 117/130


21/11/2025, 04:41 API-Football - Documentation

Copy Expand all Collapse all

```
     {

       "get": "odds/live/bets",

       "parameters": [ ],

       "errors": [ ],

       "results": 137,

             "paging": {

         "current": 1,

         "total": 1

       },

```

https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 118/130


21/11/2025, 04:41 API-Football - Documentation

```
      - "response": [

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { }
```

https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 119/130


21/11/2025, 04:41 API-Football - Documentation
```
        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

```

https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 120/130


21/11/2025, 04:41 API-Football - Documentation

```
        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

```

https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 121/130


21/11/2025, 04:41 API-Football - Documentation
```
         { },

        + { … }

       ]

     }
# Odds (Pre-Match)
```

Get odds from fixtures, leagues or date.

This endpoint uses a pagination system, you can navigate between the different pages with to the

`page` parameter.

Pagination : 10 results per page.

We provide pre ~~-~~ match odds between 1 and 14 days before the fixture.

We keep a 7 ~~-~~ days history (The availability ofodds may vary according to the leagues, seasons, fixtures

Update Frequency : This endpoint is updated every 3 hours.

Recommended Calls : 1 call every 3 hours.

QUERY PARAMETERS


```
fixture

league

season

date

timezone

```


The id of the fixture

The id of the league

The season of the league

stringYYY ~~Y-~~ MM ~~-~~ DD

A valid date

A valid timezone from the endpoint `Timezone`



https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 122/130


21/11/2025, 04:41 API-Football - Documentation


```
  page

  bookmaker

  bet

```

HEADER PARAMETERS

```
  x-apisports-key

  required

```

**200** OK

**204** No Content

**499** Time Out



Use for the pagination

The id of the bookmaker

The id of the bet



**500** Internal Server Error

GET `/odds`

Request samples

Use Cases Php Python Node JavaScript Curl Ruby

```
  // Get all available odds from one {fixture}

```



```
     get "https://v3.football.api-sports.io/odds?fixture=164327"( );

     // Get all available odds from one {league} & {season}

     get "https://v3.football.api-sports.io/odds?league=39&season=2019"( );

     // Get all available odds from one {date}

     get "https://v3.football.api-sports.io/odds?date=2020-05-15"( );

```

https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 123/130


21/11/2025, 04:41 API-Football - Documentation

```
     // It’s possible to make requests by mixing the available parameters

     get "https://v3.football.api-sports.io/odds?bookmaker=1&bet=4&league=39&seaso(

     get "https://v3.football.api-sports.io/odds?bet=4&fixture=164327"( );

     get "https://v3.football.api-sports.io/odds?bookmaker=1&league=39&season=2019(

     get "https://v3.football.api-sports.io/odds?date=2020-05-15&page=2&bet=4"( );
```

Response samples

200 204 499 500


 

Copy Expand all Collapse all

```
     {

       "get": "odds",

      - "parameters": {

         "fixture": "326090",

         "bookmaker": "6"

       },

       "errors": [ ],

       "results": 1,

             "paging": {

         "current": 1,

         "total": 1

       },

      - "response": [

        + { … }

       ]

     }
```

Get the list of available fixtures `id` for the endpoint odds.

All fixtures, leagues `id` and `date` can be used in endpoint odds as filters.

This endpoint uses a pagination system, you can navigate between the different pages with to the

`page` parameter.

Pagination : 100 results per page.


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 124/130


21/11/2025, 04:41 API-Football - Documentation

Update Frequency : This endpoint is updated every day.

Recommended Calls : 1 call per day.

QUERY PARAMETERS


```
  page

```

HEADER PARAMETERS

```
  x-apisports-key

  required

```

**200** OK

**204** No Content

**499** Time Out



Use for the pagination



**500** Internal Server Error

GET `/odds/mapping`

Request samples

Php Python Node JavaScript Curl Ruby

```
     $client = new http Client\ ;

     $request = new http Client Request\ \ ;

     $request->setRequestUrl 'https://v3.football.api-sports.io/odds/mapping'( );

     $request->setRequestMethod 'GET'( );

     $request->setHeaders array( (

          'x-apisports-key' => 'XxXxXxXxXxXxXxXxXxXxXxXx'

     ));

```

https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 125/130


21/11/2025, 04:41 API-Football - Documentation

```
     $client->enqueue $request ->( ) send();

```

```
$response = $client->getResponse

```

```
();

```

```
  echo $response->getBody
```

Response samples


```
();

```


200 204 499 500

```
  {

    "get": "odds/mapping",

    "parameters": [ ],

    "errors": [ ],

    "results": 129,

      "paging": {

      "current": 1,

      "total": 1

    },

  - "response": [

    + { …,}

    + { …,}

    + { …,}

    + { … }

    ]

  }
```

Get all available bookmakers.

All bookmakers `id` can be used in endpoint odds as filters.



Copy Expand all Collapse all



Update Frequency : This endpoint is updated several times a week.

Recommended Calls : 1 call per day.

QUERY PARAMETERS


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 126/130


21/11/2025, 04:41 API-Football - Documentation


```
  id

  search

```

HEADER PARAMETERS

```
  x-apisports-key

  required

```

**200** OK

**204** No Content

**499** Time Out



The id of the bookmaker

The name of the bookmaker



**500** Internal Server Error

GET `/odds/bookmakers`

Request samples

Use Cases Php Python Node JavaScript Curl Ruby

```
  // Get all available bookmakers

```



```
     get "https://v3.football.api-sports.io/odds/bookmakers"( );

     // Get bookmaker from one {id}

     get "https://v3.football.api-sports.io/odds/bookmakers?id=1"( );

     // Allows you to search for a bookmaker in relation to a bookmakers {name}

     get "https://v3.football.api-sports.io/odds/bookmakers?search=Betfair"( );
```

Response samples


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 127/130


21/11/2025, 04:41 API-Football - Documentation

200 204 499 500

Copy Expand all Collapse all

```
     {

       "get": "odds/bookmakers",

       "parameters": [ ],

       "errors": [ ],

       "results": 15,

             "paging": {

         "current": 1,

         "total": 1

       },

      - "response": [

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { … }

       ]

     }
```

Get all available bets for pre ~~-~~ match odds.

All bets `id` can be used in endpoint odds as filters, but are not compatible with endpoint

`odds/live` for in-play odds.

Update Frequency : This endpoint is updated several times a week.


https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 128/130


21/11/2025, 04:41 API-Football - Documentation

Recommended Calls : 1 call per day.

QUERY PARAMETERS


```
  id

  search

```

HEADER PARAMETERS

```
  x-apisports-key

  required

```

**200** OK

**204** No Content

**499** Time Out



The id of the bet name

The name of the bet



**500** Internal Server Error

GET `/odds/bets`

Request samples

Use Cases Php Python Node JavaScript Curl Ruby

```
  // Get all available bets

```



```
     get "https://v3.football.api-sports.io/odds/bets"( );

     // Get bet from one {id}

     get "https://v3.football.api-sports.io/odds/bets?id=1"( );

```

https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 129/130


21/11/2025, 04:41 API-Football - Documentation

```
     // Allows you to search for a bet in relation to a bets {name}

     get "https://v3.football.api-sports.io/odds/bets?search=winner"( );
```

Response samples

200 204 499 500

Copy Expand all Collapse all

```
     {

       "get": "odds/bets",

      - "parameters": {

         "search": "under"

       },

       "errors": [ ],

       "results": 7,

             "paging": {

         "current": 1,

         "total": 1

       },

      - "response": [

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { …,}

        + { … }

       ]

     }

```

https://www.api-football.com/documentation-v3#tag/Fixtures/operation/get-fixtures-lineups 130/130


