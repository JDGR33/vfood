# Food prices scraping for Venezuela

# Description

The aim of the project is to create a python script that scrapes food prices from the top supermarkets of Caracas, Venezuela and loads the data in a database.

Currently, I am scraping the data each day running a .bat file with Task Scheduler on my Windows PC and loading the data to a Postgres database that is locally hosted. 

The test_data.csv is a sample of the database that gives you an idea of how the database looks. In my experience the search results of the supermarkets' web pages are bad, so many unrelated products show up. Even dough the script filters out products that have no similarity with the product begin scrape, the data collected is raw and downstream process may need to clean it to fit its goals.

If you want to send messages via Telegram bot, you will first need to:
1. Create one using BotFather
2. Get its `Token`
3. Message the bot
4. Get the `Chat ID` of your Chat with it
5. Add the `Token` and `Chat ID` to `.env` (see `env_example.txt`)

For a step-step guide see [this Article](https://medium.com/codex/using-python-to-send-telegram-messages-in-3-simple-steps-419a8b5e5e2)

For example, if you scrape prices for “egg” (huevo in Spanish) you will have results like “egg pasta” (pasta de huevo).

In the future, I will deploy this project in a Linux server that will run the automation in a cron job and will host the Data Base.

If you want to run this automation yourself, you will need to create your own .bat to run the automation and your own .env with your Postgres credentials.

## Exchange Rates in Venezuela

Some supermarkets provide prices in the local currency (Bolivares) and others in US Dollars. Because the US Dollar is widely used in Venezuela for payment I decided to include a column with the prices converting the Prices from Bolivares to US Dollars using the scraped official exchange rate from Venezuela´s Central Bank Web Page. 

The exchange rate in Venezuela is a complicated topic, especially if you don´t live in the country. The water-down explanation is that there are two exchange rates: the official exchange rate (published by Venezuela´s Central Bank) and the unofficial exchange rate. These two can differ some weeks and businesses may prefer one over the other.


# Usage
If you want to use this code you will need to create a virtual environment with the dependencies of the requirements.txt.

Then you need to create a `.env` file with the credentials for your Postgres SQL database. For security reasons I don’t share mine in this repository but you can use `env_example.txt` as a template for yours. If you want to use another relational database management system, you will need to modify the `update_a_db` function in the `update_db.py` module. Remember that is the main file that runs the automation.

If you want to add or remove products, you can do it by changing `food.csv` in `ref_table`.

If you want to run the script in a schedule, I left an example of the batch file I am running and the log file it updates. If you have Windows you will want to take a look at how to setup up a Task in Task Scheduler and if you are running Linux you want to take a look at Cron jobs. 

# Roadmap
* I want python to send me a Report via Telegram when the scraping is over.
* I want to scrape the official exchange rate 3 times every day and save the data in a second database.
* I want to deploy the project on a Linux server.

# Authors and acknowledgment
Julio Guerrero is the author of this project, his email is juliodanielguerrero@gmail.com.

Special thanks to Gabriel Velasquez and Nicole Pineda for giving me the idea for this project.

# License

This project was done with an MIT license, for more information read the LICENSE file.
