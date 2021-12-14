#Info to be used for btc
# Please note that trading BTC and BNB might not work correctly
BTCINFO = ['BTCUSDT','3d',5,5,'BTC','USDT','close','open']


SIGNALS = [
  # examples change these to match your preferences
  # [pair, candle length, sma1, sma2, amount, coin1, coin2, smapoint1, smapoint2, sma1 multiplier, sma2 multiplier, group]
  # group = 0 if you dont want to group pair
  #['ETHDAI','1d',5,5,0,'ETH','DAI','close','open', 1.000, 1.002,0],
  #['NEOUSDC','1d',5,5,0,'NEO','USDC','close','open', 1.000, 1.002,0],
  ['FTMUSDT','4h',5,5,0,'FTM','USDT','close','open', 1.000, 1.000,0],
  ['HBARBUSD','4h',5,5,0,'HBAR','BUSD','close','open', 1.000, 1.000,1],
  ['ICPBUSD','4h',5,5,0,'ICP','BUSD','close','open', 1.000, 1.000,1],
  ['LTOBUSD','4h',5,5,0,'LTO','BUSD','close','open', 1.000, 1.000,1],
  ['ROSEBUSD','4h',5,5,0,'ROSE','BUSD','close','open', 1.000, 1.000,1],
  ['LTCTUSD','4h',5,5,0,'LTC','TUSD','close','open', 1.000, 1.000,2],
  ['PHBTUSD','4h',5,5,0,'PHB','TUSD','close','open', 1.000, 1.000,2],
  ['BTTTUSD','4h',5,5,0,'BTT','TUSD','close','open', 1.000, 1.000,2],
  #['LINKTUSD','1d',5,5,0,'LINK','TUSD','close','open', 1.000, 1.002,2]
]

#set time bot waits 
# after every round
SLEEPTIME = 45
# after every coin
SLEEPTIME2 = 10

#percentage to use as a "stop loss" and to set price where bot can trade next time. Ie. if bought at 1.00$ and stoploss is 10 bot will onlys sell if price is over 1.1 or under 0.9
STOPLOSS = 3


#max decimals, check binance for correct decimals or use decimal that gives approx 1$ - 9$. Ie. if token price is 23$ decimal 1 should be ok to be used
DECIMALS = {
  'BTC':5,
  'BNB':3,
  'USDT':2,
  'BUSD':2,
  'USDC':2,
  'XRP':0,
  'DOT':2,
  'XVS':3,
  'CREAM':3,
  'DENT':0,
  'DAI':2,
  'DOGE':0,
  'XLM':0,
  'FTM':1,
  'TUSD':2,
  'ETH':4,
  'BTCUP':2,
  'BTCDOWN':2,
  'LINK':2,
  'AAVE':3,
  'LTC':4,
  'EGLD':3,
  'BAT':2,
  'IOTA':1,
  'REEF':1,
  'ROSE':1,
  'NEO':1,
  'ADA':1,
  'BTT':0,
  'HBAR':0,
  'LTO':0,
  'ICP':1,
  'PHB':0,
  'SOL':2
}

versio='1.2btc'
tyyppi = 'MARKET'
balance=0
sma_values = {}
tiedot = []