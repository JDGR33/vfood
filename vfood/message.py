"""
Functions to send messages
"""
import os
from dotenv import load_dotenv
import requests
from datetime import datetime
import re


def telegram_message(message:str,mk=True):
    """Send a Telegram message.
    
    Reads the Bot token  and the chat id of the chat from a .env to send a message to a Telegram user. 

    Parameters
    ----------
    message : str
        The message that will be send to the Chat.
    mk : bool
        True to activate MarkdownV2  parser, false otherwise.
    """
    assert isinstance(message,str)
    
    #Load Telegram bot credentials
    load_dotenv()
    TOKEN = os.getenv("TELEGRAM_TOKEN") #Bot token
    CHAT_ID = os.getenv("TELEGRAM_CHAT_ID") #Chat where the message will be send
    
    if mk:
        message= prep_message_mk(message)
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}&parse_mode=MarkdownV2"
    else :
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

    message = f"📊 At *{dt_string}* these foods were scraped:"
    #Make a list of all the foods in the message
    for food in foods:
        message = message +f"\n\t• {food}"

    #Ads extra information at the end of the Message
    if len(argv)>0:
        message = message + "\n\n⁉Extra information"
        for arg in argv:
            message = message + "\n\t• "+str(arg)
    
    assert isinstance(message,str)

    return message

def create_message_exchange(rates_data:list)->str:
    """Create a Telegram message with the data of all the exchange rates.
    
    Parameters :
    ------------
    rates_data : list
        A list of dictionaries with the information for each exchange rate.

    
    Returns :
    ---------
    str :
        The Telegram message    
    """

    if len(rates_data)<1:
        raise ValueError("rates_data must have at lest 1 element.")

    
    message = "*💵Exchange Rate Report:*"
    for rate_data in rates_data:
        
        if not(isinstance(rate_data,dict)):
            raise TypeError("One of the elements is not a dict.")

        exchange_rate = rate_data['exchange_rate'][0]
        date_exchange = rate_data['date'][0].strftime("%Y-%m-%d %H:%M")
        source = rate_data['source'][0]
        
        message = message + f"\n\t•The exchange rate is *{exchange_rate}* Bs/$ according to *{source}* at {date_exchange}"
    
    print(message)

    return(message)
        
def prep_message_mk(og_txt:str)->str:
    """Prepare a string for Telegram Markdown parser.
    
    Parameters :
    ------------
    og_txt : str
        The string to prepare

    Returns :
    ---------
    A string for Telegram Markdown parser.
    """
    special_chrs = ['\[', '\]', '\(', '\)','>', '#', '\+', '-', '=', '\{', '\}', '\.', '!']

    for chr in special_chrs :
        
        print(og_txt)
        og_txt = re.sub(chr,"\\"+chr ,og_txt)
        print(chr)

    return og_txt

# #txt = prep_message_mk("[_*[]()~`>#+-=|{}.!,]")
# telegram_message("[_*[]()~`>#+-=|{}.!,]")




