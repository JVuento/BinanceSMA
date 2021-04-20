SIGNALS = [
  # examples change these to match your preferences
  # [pair, candle length, sma1, sma2, amount, coin1, coin2, smapoint1, smapoint2, sma1 multiplier, sma2 multiplier, group]
  # group = 0 if you dont want to group pair
  #['BNBTUSD','4h',5,5,1,'BNB','TUSD','close','open', 1.000, 1.002,0],
  #['ETHDAI','4h',5,5,0,'ETH','DAI','close','open', 1.000, 1.002,0],
  #['LINKUSDC','4h',5,5,0,'LINK','USDC','close','open', 1.000, 1.003,0],
  #['XRPBUSD','4h',5,5,0,'XRP','BUSD','close','open', 1.000, 1.002,1],
  #['XLMBUSD','4h',5,5,0,'XLM','BUSD','close','open', 1.000, 1.002,1],
  #['BTCUPUSDT','4h',5,5,0,'BTCUP','USDT','close','open', 1.000, 1.003,2],
  #['BTCDOWNUSDT','4h',5,5,0,'BTCDOWN','USDT','close','open', 1.000, 1.003,2]
  ['BNBDAI','2h',5,5,0.8,'BNB','DAI','close','open', 1.000, 1.002,0],
  ['BTCTUSD','2h',5,5,0,'BTC','TUSD','close','open', 1.000, 1.002,1],
  ['LTCTUSD','2h',5,5,0,'LTC','TUSD','close','open', 1.000, 1.002,1],  
  ['XRPUSDC','2h',5,5,0,'XRP','USDC','close','open', 1.000, 1.002,2],
  ['NEOUSDC','2h',5,5,0,'NEO','USDC','close','open', 1.000, 1.002,2],
  ['XLMBUSD','2h',5,5,0,'XLM','BUSD','close','open', 1.000, 1.002,3],
  ['AAVEBUSD','2h',5,5,0,'AAVE','BUSD','close','open', 1.000, 1.002,3],
  ['DENTUSDT','2h',5,5,0,'DENT','USDT','close','open', 1.000, 1.002,4],
  ['EGLDUSDT','2h',5,5,0,'EGLD','USDT','close','open', 1.000, 1.002,4],
  ['DOGEUSDT','2h',5,5,0,'DOGE','USDT','close','open', 1.000, 1.002,4],
  ['LINKUSDT','2h',5,5,0,'LINK','USDT','close','open', 1.000, 1.002,4]
  
]

#set time bot waits before fetching new values
SLEEPTIME = 45

#set how many decimals can be used for each coin, check from binance how many decimals is allowed in buy of that coin
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
  'DAI':2,
  'DOGE':0,
  'XLM':1,
  'TUSD':2,
  'ETH':5,
  'BTCUP':2,
  'BTCDOWN':2,
  'LINK':2,
  'AAVE':3,
  'LTC':5,
  'EGLD':3,
  'NEO':3
}