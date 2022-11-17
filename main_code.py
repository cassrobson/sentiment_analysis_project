import datetime, requests
from alpaca_trade_api.rest import REST
from transformers import pipeline
import yfinance as yf
import mplfinance


#Create base_url so the program can reference either paper trading or alpaca trading broker
#Input your API Keys

BASE_URL = "https://paper-api.alpaca.markets"
API_KEY = 'PK00Q604ZSKD91W2PFR9'
SECRET_KEY ='xyjs4SmqBEufSEogRuOmcSCl5Aj3q30a5iSkcrY4'

#Specify order dollar amount and ticker
ORDER_DOLLAR_SIZE = 2000
SYMBOL = "TSLA"

#Initialize counters
negative_counter = 0
positive_counter = 0

#create a rest object with keys and url
api = REST(key_id=API_KEY, secret_key=SECRET_KEY, base_url=BASE_URL)

#use alpaca's news api to get news on specified ticker
news = api.get_news(SYMBOL)



classify = pipeline('sentiment-analysis')

#iterate through news and print headlines
print()
print()
for story in news:
    print('---------------------------------------------------------------------------------------')
    print(story.headline, " | Created at: ", story.created_at, "| Written by: ", story.author)
    #put the article headline through the sentiment analysis headline and output results
    connotation = classify(story.headline)
    print("Overall Connotation ----> ", connotation[0].get('label'), " | ",  "Score -----> ", float(connotation[0].get('score') * 100), "%")

    #identify headlines that are negative or positive with a score above 95%
    if str(connotation[0].get('label')) == "NEGATIVE" and float(connotation[0].get('score')) > 0.95:
        negative_counter += 1
    elif str(connotation[0].get('label')) == "POSITIVE" and float(connotation[0].get('score')) > 0.95:
        positive_counter += 1


#display counters

print()
print("NEGATIVE COUNTER ---->", negative_counter)
print()
print("POSITIVE COUNTER ---->", positive_counter)
print()


#if there are more positive counters than regular counters, we buy the stock and hold long

if positive_counter > negative_counter:
    print("BUYING {} STOCK DUE TO POSITIVE NEWS RELEASED ABOUT THE COMPANY".format(SYMBOL))
    order = api.submit_order("TWTR", 10, "buy", "market", "gtc")
    print("SUCCESSFULLY SUBMITTED ORDER WITH ORDER_ID {}".format(order.id))


#otherwise we short the stock based on its current price. Assuming that the bad news will cause owners to dump their stock
elif negative_counter > positive_counter:
    
    stock = yf.Ticker(SYMBOL)
    quotes = stock.info['regularMarketPrice']
    
    quantity = ORDER_DOLLAR_SIZE // quotes
    take_profit = round(quotes * 0.99, 2)
    stop_price = round(quotes * 1.01, 2)
    stop_limit_price = round(quotes * 1.02, 2)

    print("CURRENT TIME: {} | SHORTING {} SHARES OF {} at {}".format(datetime.datetime.now().isoformat(), quantity, SYMBOL, quotes))

    try: 
        order_short = api.submit_order(SYMBOL, quantity, 'sell', 
                                    order_class='bracket', 
                                    take_profit={
                                        'limit_price': take_profit
                                    }, 
                                    stop_loss={
                                        'stop_price': stop_price, 
                                        'limit_price': stop_limit_price
                                    })
        print("SUCCESSFULLY SUBMITTED ORDER WITH ORDER_ID {}".format(order_short.id))
    except Exception as e:
        print("error executing the above order {}".format(e))



