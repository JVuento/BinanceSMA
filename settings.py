SIGNALS = {
  #examples change these to match your preferences
  #'BTCUSDT': ['1h',2,3,0,'BTC','USDT'],
  'BTCUSDT': ['1h',5,12,0,'BTC','USDT'],
  'BAKEBUSD': ['4h',2,4,200,'BAKE','BUSD'],
  'DODOBUSD': ['4h',2,4,54,'DODO','BUSD'],
  'DOTBUSD': ['4h',2,4,5.35,'DOT','BUSD'],
  'XVSBUSD': ['4h',2,4,2,'XVS','BUSD'],
  'LINKBUSD': ['4h',2,4,1.61,'LINK','BUSD'],
  'XMRBUSD': ['4h',2,4,0.4,'XMR','BUSD']
}

#set deafult pair used if run without argument
DEFPAIR = 'DODOBUSD'

#set time bot waits before fetching new values
SLEEPTIME = 180