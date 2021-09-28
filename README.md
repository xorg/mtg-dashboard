 # mtg-dashboard
Simple Magic the Gathering Dashboard to monitor card values of your collection. Built with Python/Flask and Vue3
![main dashboard screen](https://github.com/xorg/mtg-dashboard/blob/media/main_screen.png)

# Requirements
- docker
- docker-compose

# Installation
```
./load-dotenv.sh
docker-compose --env=.env up
```
   
This starts the front- and backend and sets up the database. The frontend is accessible at `127.0.0.1:3000`

# Testing and Coverage
```
docker-compose run backend coverage run -m pytest
docker-compose run backend coverage report
# or
docker-compose run backend coverage html
```

# How it works
This app consists of following parts:

## Backend
The backend gathers all the data it needs from the database and prepares it for the frontend.

## Crawler
This is how new cards are imported into the database. The crawler is intended to run once to import new files and then run daily via cron job to update all card prices in the database

### How to use the crawler
Import new files
```
docker-compose run flask crawler import ./tests/fixtures/test_import_data.txt
```

Update existing files (this may take a while)
```
docker-compose run flask crawler import ./tests/fixtures/test_import_data.csv
```

## Database
The Database holds all card and collection related data


## Frontend
This is the face of the dashboard and displays all the nice data. The frontend is adapted from the [Tailmin Admin Dashboard](https://github.com/otezz/tailmin). It shows a chart for every collection displaying the value over time.

# Data model

The data model consists of four pieces: Collection Card and Price.

## Collection

A Collection is a simple unit of cards that you want to track. This might be a specific set you collected or a deck of cards that you might want to track the value of. A collection only has a name and can contain any number of cards

## Card
A single card. This holds all information related to one card, such as name, set and count. A card can be in different collections and relates to different prices (for different time points).

## Price
The price of a card at a specific point in time. All prices of a card in chronological order make a nice graph.
