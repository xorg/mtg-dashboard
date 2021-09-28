 # mtg-dashboard
Simple Magic the Gathering Dashboard to monitor card values of your collection. Built with Python/Flask and Vue3.
![main dashboard screen](https://github.com/xorg/mtg-dashboard/blob/media/main_screen.png)

mtg-dashboard allows you to import your Magic card collection and continously track the the monetary value of your cards. A convenient dashboard displays important data such as the value of the different collections over time or the most valuable cards.

A crawler allows keeping the local database up to date and

# Requirements
- docker
- docker-compose

# Installation
```
./load-dotenv.sh
docker-compose up
```

This starts the front- and backend and sets up the database. The frontend is accessible at `http://localhost:3000`. The backend can be found at `http:/localhost:5000`

# Testing and Coverage
```
docker-compose run backend coverage run -m pytest

docker-compose run backend coverage report # or
docker-compose run backend coverage html
```

# How it works
This app consists of following parts:

## Backend
The backend gathers all the data it needs from the database and prepares it for the frontend. It's built using Python and Flask.

## Crawler
This is how new cards are imported into the database. The crawler is intended to run once to import new files and then run daily via cron job to update all card prices in the database. The crawler connects to the [Scryfall API](https://scryfall.com/docs/api) and fetches all data from there.

#### How to use the crawler
Import new files
```
docker-compose run flask crawler import ./tests/fixtures/test_import_data.txt
```

Update existing files (this may take a while)
```
docker-compose run flask crawler import ./tests/fixtures/test_import_data.csv
```

To update the database once a day, add following cron job to your crontab:
`0 4 * * * cd <path_to_project> && docker-compose run backend flask crawler update >> /var/log/mtg_dashboard_cron.log 2>&1`


## Database
The Database holds all card and collection related data. I am using a Postgres 13.2 database and the backend connects to it through a SQLAlchemy ORM layer.


## Frontend
This is the face of the dashboard and displays all the nice data. The frontend is adapted from the [Tailmin Admin Dashboard](https://github.com/otezz/tailmin) template and uses Vue.js v3 as well as the Tailwind CSS framework.

As the queries for the charts, stats and other data take quite a while, the dashboard fully loads after about 4-10 seconds. The page itself loads much faster, thanks to the asynchronous accessing of the backend api.

The UI consists of different parts:

### Stats
![stats](https://github.com/xorg/mtg-dashboard/blob/media/stats.png)
A dashboard needs nice stats...

### Graphs
![graphs](https://github.com/xorg/mtg-dashboard/blob/media/graphs.png)
...and nice Charts! For every collection in the database there is a chart tracking the price of the total value of a collection.

### Top cards
![cards](https://github.com/xorg/mtg-dashboard/blob/media/top_cards.png)
Lists the most valuable card in the database in descending order. Clicking on the card name opens a card picture.

### Sidebar
![sidebar](https://github.com/xorg/mtg-dashboard/blob/media/sidebar.png)
A Sidebar. Almost empty at the moment but can hold menu items for future additional  dashboard screens.

# Data model

The data model consists of three objects: Collection, Card and Price.

### Card
A single card. This holds all information related to one card, such as name, set and count. A card can be in different collections and relates to different prices (for different time points).

A card relates to many prices, one for every point in the the crawler was run to update the prices. Ideally every data point should be more or less one day apart. The prices are sorted descending by date, meaning the first item in the price list of a card is the last crawled price.

Cards don't have a field for the current price, this is queried on the fly using SQLAlchemy's hybrid attributes. These attributes behave like normal attributes and can be sorted, queried, accessed like it would be a database column. Except it's not a column, it's translated to a SQL query with every access.
This makes complex hybrid attributes a bit slow.


### Collection

A Collection is a simple unit of cards that you want to track. This might be a specific set you collected or a deck of cards that you might want to track the value of. A collection only has a name and can contain any number of cards.

The collection's current value (`value`) as well as it's value over time (`value_history`) is queried on the fly with hybrid attributes. As there queries are pretty complex the queries are pretty slow.


### Price
The price of a card at a specific point in time. All prices of a card in chronological order make a nice graph. Every price has a date, a price and is linked to exactly one card.

# Considerations
Starting the project out, I felt very clever using hybrid attributes for things such as the current price of a card or the value of a collection over time.
During the project realized that those hybrid attribute queries have to be executed _a lot_, and they take forever once there are a few data points. This is the reason the frontend's loading time is about 4-10 seconds.

With more time I would've optimised the queries to run faster or just use static fields and keep them up to date them with triggers every time a new price is added.

What didnt make the finish line as well was single card charts. It wouldve been cool to make the top card panel a accordion with a chart expanding under every card when clicked. But maybe this is something for version 2.0 ;)

The time wasn't enough to add card import through the frontend. At the moment this has to be done with the crawler. This works, but it's a bit clunky and not as easy as just using the dashboard directly. 

A loading animation for the frontend would've been nice as well. As it stands now, the first page load doesn't really look good until the chart and stats data arrive. 

Lastly the backend doesn't do much error handling. As almost all endpoints are read only and there's no input. With more time I wouldve implemented actual error pages with user friendly messages.

