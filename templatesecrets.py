#Rename to secrets.py and update your secrets.
#---------------------------------------------
#Never give these to anyone else!!!!
#Secrets.py is included in gitignore, still be sure not to update your keys etc to anywhere!!!

#api keys, you get these from binance while crerating new api
API_KEY='KEY'
API_SECRET='SECRET'

# what MA-figures you want a bot to follow and what trade also indicates the amount to buy (if 0 then all awailable)
# also pair is opened in here, to help parsee coins traded
# format: {'PAIR': ['CANDLETIME', MA1, MA2, AMOUNT,'COIN1', 'COIN2']}
SIGNALS = {
  #examples change these to match your preferences
  'BTCUSDT': ['1h',2,12,0,'BTC','USDT'],
  'XLMBUSD': ['15m',5,15,20,'XLM','BUSD']
}
