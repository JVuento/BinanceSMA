SIGNALS = [
  # examples change these to match your preferences
  # [pair, candle length, sma1, sma2, amount, coin1, coin2, smapoint1, smapoint2, sma1 multiplier, sma2 multiplier, group]
  # group = 0 if you dont want to group pair

  ['BTCUSDC','4h',5,5,0,'BTC','USDT','close','open', 1.000, 1.003, 1],
  ['XRPUSDC','4h',5,5,0,'XRP','USDC','close','open', 1.000, 1.003,1],
  ['XVSBUSD','4h',5,5,2,'XVS','BUSD','close','open', 1.000, 1.003,2],
  ['DENTUSDT','4h',5,5,2000,'DENT','USDT','close','open', 1.000, 1.003,2]
  
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