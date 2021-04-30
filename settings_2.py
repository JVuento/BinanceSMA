SIGNALS = [
  # examples change these to match your preferences
  # [pair, candle length, sma1, sma2, amount, coin1, coin2, smapoint1, smapoint2, sma1 multiplier, sma2 multiplier, group]
  # group = 0 if you dont want to group pair
  #['BNBDAI','4h',5,5,0.6,'BNB','DAI','close','open', 1.000, 1.003,0],
  #['BTCTUSD','4h',5,5,0,'BTC','TUSD','close','open', 1.000, 1.003,0],
  #['FTMUSDT','4h',5,5,0,'FTM','USDT','close','open', 1.000, 1.003,0],
  ['BATUSDC','1h',5,5,75,'BAT','USDC','close','open', 0.999, 1.003,0]
  #['XRPBUSD','4h',5,5,0,'XRP','BUSD','close','open', 1.000, 1.002,1]
]

#set time bot waits before fetching new values
SLEEPTIME = 45
SELLSTOP = 1.08
BUYSTOP = 0.92

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
  'FTM':1,
  'TUSD':2,
  'ETH':5,
  'BTCUP':2,
  'BTCDOWN':2,
  'LINK':2,
  'AAVE':3,
  'LTC':5,
  'EGLD':3,
  'BAT':2,
  'NEO':3
}

versio='3.0000'
tyyppi = 'MARKET'
balance=0
sma_values = {}
tiedot = []