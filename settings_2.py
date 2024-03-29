SIGNALS = [
  # examples change these to match your preferences
  # [pair, candle length, sma1, sma2, amount, coin1, coin2, smapoint1, smapoint2, sma1 multiplier, sma2 multiplier, group]
  # group = 0 if you dont want to group pair
  ['BTCDAI','8h',5,5,0,'BTC','DAI','close','open', 1.000, 1.003,0],
  ['ICPUSDT','8h',5,5,0,'ICP','USDT','close','open', 1.000, 1.003,0],
  ['DOGEBUSD','8h',5,5,0,'DOGE','BUSD','close','open', 1.000, 1.003,0],
  ['ETHUSDC','8h',5,5,0,'ETH','USDC','close','open', 1.000, 1.003,0],
  ['XRPPAX','8h',5,5,0,'XRP','PAX','close','open', 1.000, 1.003,0],
  ['DOTBIDR','8h',5,5,0,'DOT','BIDR','close','open', 1.000, 1.003,0],
  ['ADATUSD','8h',5,5,0,'ADA','TUSD','close','open', 1.000, 1.003,0]
]

#set time bot waits before fetching new values
SLEEPTIME = 45
SELLSTOP = 1.10
BUYSTOP = 0.90

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
  'ONE':1,
  'ADA':2,
  'WAVES':3,
  'BIDR':0,
  'PAX':4,
  'ICP':2,
  'NEO':3
}

versio='3.0000'
tyyppi = 'MARKET'
balance=0
sma_values = {}
tiedot = []