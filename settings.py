SIGNALS = [
  #examples change these to match your preferences
  #[pair, candle length, sma1, sma2, amount, coin1, coin2, smapoint1, smapoint2, sma1 multiplier, sma2 multiplier]

  ['BTCDAI','4h',5,5,0,'BTC','DAI','close','open', 1.000, 1.002],
  ['XRPUSDC','4h',5,5,0,'XRP','USDC','close','open', 1.000, 1.002],
  ['CREAMBUSD','4h',5,5,1,'CREAM','BUSD','close','open', 1.000, 1.004],
  ['DENTUSDT','4h',5,5,5000,'DENT','USDT','close','open', 1.000, 1.004],
  ['BNBBUSD','4h',5,5,1,'BNB','BUSD','close','open', 1.000, 1.002]
  #['DOTBUSD','4h',5,5,4,'DOT','BUSD','close','open', 1.000, 1.002],
  #['XVSBUSD','4h',4,4,1,'XVS','BUSD','close','open', 1.000, 1.002]
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
  'XVS':3,
  'CREAM':3,
  'DENT':0,
  'DAI':2
}