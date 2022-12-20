# load data to SQL server

#import pyodbc
import sqlalchemy as sal
from sqlalchemy import create_engine
import pandas as pd

df = pd.read_excel("prueba.xlsx").drop(columns=['Unnamed: 0'])
df = df.rename(columns={'product_name':"name","product_price":"price_label","product_availability":"availability"\
                        ,"date":"date_scrapt","store":"store_name","product_price_dollar":"price_dollar"})
df['date_scrapt'] = pd.to_datetime(df['date_scrapt'])
print("Shape of table " +str(df.shape))
print(df.head())
engine = create_engine('postgresql://postgres:clave1234@localhost:5432/price_scrapt')

df.to_sql("food",con=engine,if_exists='append',index=False)
print("Complete")