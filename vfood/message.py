"""
Functions to send messages
"""
import os
from dotenv import load_dotenv
import requests
from datetime import datetime


def telegram_message(message:str):
    """Send a Telegram message.
    
    Reads the Bot token  and the chat id of the chat from a .env to send a message to a Telegram user. 

    Parameters
    ----------
    message : str
        The message that will be send to the Chat.
    """
    assert isinstance(message,str)
    
    #Load Telegram bot credentials
    load_dotenv()
    TOKEN = os.getenv("TELEGRAM_TOKEN") #Bot token
    CHAT_ID = os.getenv("TELEGRAM_CHAT_ID") #Chat where the message will be send
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"

    assert isinstance(url,str)
    try:
        print(requests.get(url).json())
    except Exception as e:
        print("Error trying to send Telegram message"+str(Exception))

def create_message_food(foods:list,*argv)->str:
    """Create the text to be send with the foods that where scrape
    
    Parameters
    ----------
    foods : list
        The list of foods that where scrape.

    *argv 
        Extra strings that will message will have.

    Returns
    -------
    str :
        The created message
    """

    dt_string = datetime.now().strftime("%Y-%m-%d %H:%M")
    message = f"At {dt_string} these foods were scraped:"
    #Make a list of all the foods in the message
    for food in foods:
        message = message +f"\n• {food}"

    #Ads extra information at the end of the Message
    if len(argv)>0:
        message = message + "\n\n Extra information"
        for arg in argv:
            message = message + "\n• "+str(arg)
    
    assert isinstance(message,str)

    return message

# ------ For Testing
#import update_db
# if __name__ == "__main__":
#     cwd = os.getcwd()
    
#     #Get the list of foods to scrap
#     food_list_path = os.path.join(cwd,'ref_table','foods.csv')
#     food_list = update_db.get_list_foods(food_list_path)

#     message = create_message(food_list,"El precio del dolar es 34","No se ha encontrado forma de procesar los datos")
#     print(message)
#     telegram_message(message)