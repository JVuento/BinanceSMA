SIGNALS = [
  #examples change these to match your preferences
  #[pair, candle length, sma1, sma2, amount, coin1, coin2, smapoint1, smapoint2, sma1 multiplier, sma2 multiplier]
  #'BTCUSDT': ['1h',2,3,0,'BTC','USDT'],
  ['BTCUSDT','1h',5,5,0,'BTC','USDT','close','open', 1.000, 1.003],
  ['XRPUSDC','1h',5,5,0,'XRP','USDC','close','open', 1.000, 1.003],
  ['DOTBUSD','1h',5,5,5.35,'DOT','BUSD','close','open', 1.000, 1.003],
  ['BNBBUSD','1h',5,5,1,'BNB','BUSD','close','open', 1.000, 1.003],
  ['XVSBUSD','1h',5,5,2,'XVS','BUSD','close','open', 1.000, 1.003]
  #'LINKBUSD': ['4h',2,4,1.61,'LINK','BUSD'],
  #'XMRBUSD': ['4h',2,4,0.4,'XMR','BUSD']
]

#set deafult pair used if run without argument
DEFPAIR = 'XVSBUSD'

#set time bot waits before fetching new values
SLEEPTIME = 45


DECIMALS = {
  'BTC':6,
  'BNB':3,
  'USDT':2,
  'BUSD':2,
  'USDC':2,
  'XRP':1,
  'DOT':2,
  'XVS':3
}