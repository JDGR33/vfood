# load data to SQL server

#import pyodbc
import sqlalchemy as sal
from sqlalchemy import create_engine
import pandas as pd
import os
from dotenv import load_dotenv


#----To do list
# Create .env for database credentials 
# Create a git ignore
# Delete commit history
# Truncate decimals of convertion in database and in pandas manipulation
# Import and use data module
# Create a .cmd schedule command
# Create a function and a database to just get the data of dollar price 

def update_db(data:pd.DataFrame,user:str,password:str,host:str,port:str,db_name:str,table_name:str):

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db_name}')

    df.to_sql(table_name,con=engine,if_exists='append',index=False)
    print("Complete")

df = pd.read_excel("prueba.xlsx").drop(columns=['Unnamed: 0'])
df = df.rename(columns={'product_name':"name","product_price":"price_label","product_availability":"availability"\
                        ,"date":"date_scrapt","store":"store_name","product_price_dollar":"price_dollar"})
df['date_scrapt'] = pd.to_datetime(df['date_scrapt'])
print("Shape of table " +str(df.shape))
print(df.head())

load_dotenv()

USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
db_name = "price_scrapt"
table_name = "food"
update_db(df,USER,PASSWORD,HOST,PORT,db_name,table_name)