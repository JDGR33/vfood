# python packages
from sqlalchemy import create_engine
import pandas as pd
import os
from dotenv import load_dotenv
# local modules
import data 
import message
from exchange_tw import exchange_from_tw_user


def update_a_db(data:pd.DataFrame,user:str,password:str,host:str,port:str,db_name:str,table_name:str):
    """Update a Postgresql table with the input data and the given credentials.

    Parameters
    ----------
    data : pd.DataFrame
        Data to be appended to the database. The columns must have the same name as the Data Bases.

    user : str
        The user for the Postgresql database.
    host : str
        The host for the Postgresql database.
    port : str
        The port for the Postgresql database.
    db_name : str
        The name of the Data Base where the table you want to update is.
    table_name : str
        The name of the Table that you want to update. 
    """

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db_name}')
    data.to_sql(table_name,con=engine,if_exists='append',index=False)

def prepare_food_data(scrapt_food_data:pd.DataFrame)->pd.DataFrame:
    """Prepare the food price data to fit with the database table schema.

    Parameters:
    -----------
    scrapt_food_data : pd.DataFrame
	    Data from the web scraping process.

    Returns:
    --------
    pd.DataFrame
	    Data ready to be appended to the database table
    """
    
    scrapt_food_data = scrapt_food_data.rename(columns={'product_name':"name","product_price":"price_label","product_availability":"availability"\
                            ,"date":"date_scrapt","store":"store_name","product_price_dollar":"price_dollar"})
    scrapt_food_data['date_scrapt'] = pd.to_datetime(scrapt_food_data['date_scrapt'])
    #print("Shape of table " +str(scrapt_food_data.shape))
    #print(scrapt_food_data.head())
    return scrapt_food_data

def prepare_bcv_data(raw_bcv_data:dict,rename={'date':'datetime','exchange_rate':'rate',"source":"nmae"})->pd.DataFrame:
    """Prepare the raw data from the bcv for the table in the database

    Parameters:
    -----------
    raw_bcv_data : dict
        The result of scraping the exchange rate from the bcv

    rename : dict
        For renaming the columns
     
    Returns:
    --------
    pd.DataFrame
        A clean DataFrame ready to be loaded to the data base
    """
    for k, v in raw_bcv_data.items():
        raw_bcv_data[k]=[v]

    rate_bcv = pd.DataFrame.from_dict(raw_bcv_data)[['date','exchange_rate','source']]
    rate_bcv = rate_bcv.rename(columns=rename)
    return(rate_bcv)

def prepare_tw_data(raw_tweet_data:dict,rename={'date':'datetime','exchange_rate':'rate',"source":"nmae"})->pd.DataFrame:
    """Prepare the raw data from the bcv for the table in the database

    Parameters:
    -----------
    raw_tweet_data : dict
        The result of scraping the exchange rate from the tweets

    rename : dict
        For renaming the columns
     
    Returns:
    --------
    pd.DataFrame
        A clean DataFrame ready to be loaded to the data base
    """
    for k, v in raw_tweet_data.items():
        raw_tweet_data[k]=[v]
    
    keep_col =['date','exchange_rate','source']
    rate_tw = pd.DataFrame.from_dict(raw_tweet_data)[keep_col]
    rate_tw = rate_tw.rename(columns=rename)
    return(rate_tw)

def get_list_foods(path:str)->list:
    """Get the list of food to scrap.
    Parameters:
    -----------
    path : str
        File path to a .csv that list all the foods to scrap for. The first column must be the one listing the foods names.
    
    Returns:
    --------
    list :
        A list object with the names of all the food to scrap.
    """
    foods = pd.read_csv(path)
    return foods.iloc[:,0].to_list()

def log_food(food_list:str,file:str):
    """Register the list of food scrap in a log file.
    Parameters:
    -----------
    food_list : str
        The list of foods to log.

    file : str
        The file path to log you want so safe the food_list.
    """
    with open(file,'a') as log_file:
        log_file.write(food_list+"\n")

def update_exchange():
    """Updates de Table for the Exchange Rate"""

    #Get DataBase credentials from a .env
    load_dotenv()
    USER = os.getenv("USER")
    PASSWORD = os.getenv("PASSWORD")
    HOST = os.getenv("HOST")
    PORT = os.getenv("PORT")

    # Table and DataBase name to safe the scrap exchange Rate of the bcv
    db_name = "price_scrapt"
    table_name = "exchange"

    #Get raw data from the bcv and preparing it for the Database
    rate_bcv_r =data.bcv_exchange_rate()
    rate_bcv = prepare_bcv_data(rate_bcv_r)
    print(rate_bcv)

    #Get raw data from the Twitter and preparing it for the Database
    rate_tw_r = exchange_from_tw_user("monitordolarvla")
    rate_tw = prepare_tw_data(rate_tw_r)
    print(rate_tw)

    # Update food Table in the DataBase
    update_a_db(pd.concat([rate_bcv,rate_tw]),USER,PASSWORD,HOST,PORT,db_name,table_name)

    #Send a message informing the end of the Scrape
    # exchange_rate = rate_bcv_r['exchange_rate'][0]
    # exchange_rate_msm = "💵Exchange Rate Report:"
    # exchange_rate_msm = exchange_rate_msm + f"\n\t•The exchange rate is {exchange_rate} Bs/$ according to BCV"

    # #Information form Twitter
    # exchange_rate = rate_tw_r['rate'][0]
    # date_exchange = rate_tw_r['date'][0].strftime("%Y-%m-%d %H:%M:%S")
    # exchange_rate_msm = exchange_rate_msm + f"\n\t•The exchange rate is {exchange_rate} Bs/$ according to monitordolarvla {date_exchange}"
    
    #print("create exchange rate message")
    exchange_rate_msm =message.create_message_exchange([rate_bcv_r,rate_tw_r])

    print(exchange_rate_msm)
    message.telegram_message(exchange_rate_msm,)

def update_foods():
    """Scrape the list of foods and update the table in the DataBase."""

    cwd = os.getcwd()
    
    #Get the list of foods to scrap
    food_list_path = os.path.join(cwd,'ref_table','foods.csv')
    food_list = get_list_foods(food_list_path)

    #Scrap the list of foods
    scrap_data = data.scrape_prep_data(food_list)
    scrap_data.to_csv("test_data.csv")

    #Prepare the scrap data for the DataBase Table
    scrap_data = prepare_food_data(scrap_data)

    #Get DataBase credentials from a .env
    load_dotenv()
    USER = os.getenv("USER")
    PASSWORD = os.getenv("PASSWORD")
    HOST = os.getenv("HOST")
    PORT = os.getenv("PORT")

    # Table and DataBase name to safe the scrap food data
    db_name = "price_scrapt"
    table_name = "food"

    # Update food Table in the DataBase
    update_a_db(scrap_data,USER,PASSWORD,HOST,PORT,db_name,table_name)

    #Log the foods that where scrap
    log_file = os.path.join(cwd,'batch.log')
    log_food(str(food_list),log_file)

    #Send a message informing the end of the Scrape
    exchange_rate = data.bcv_exchange_rate()['exchange_rate']
    source = data.bcv_exchange_rate()['source']
    exchange_rate_msm = f"The exchange rate is *{exchange_rate}* Bs./$ according  to the *{source}*"
    message_txt = message.create_message_food   (food_list,exchange_rate_msm)
    print(message_txt)
    message.telegram_message(message_txt,)