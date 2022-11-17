# Sentiment Analysis Trading Project

This program performs sentiment analysis on the 10 most recent articles relating to a specified Ticker. It uses a transformer pipeline to determine the connotation (positive, negative) and gives it a score out of 100 regarding the strength of connotation. 

Out of the 10 articles, if the program finds there to be more negative articles than positive, the program predicts that shareholders will dump their shares in result of the recent news, and shorts the stock, taking a profit once the stop price is reached.

If the program finds there to be more positive articles, the program buys the stock, assuming the share price will prosper after the release of recent articles. 
