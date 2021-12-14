#==============================================================================================================#
# BinaceSMA.py  
# small bot to trade in binance with help of SMA x 2
#
#
# Before run make sure you have bfx-hf-indicators-p and python-binance installed in you python : 
#  pip install git+https://github.com/bitfinexcom/bfx-hf-indicators-py 
#  pip install python-binance
#  OR
#  pip3 install git+https://github.com/bitfinexcom/bfx-hf-indicators-py 
#  pip3 install python-binance
#  more info about python-binance lib here: https://algotrading101.com/learn/binance-python-api-guide/
#
#  For python anywhere:
#  pip3.8 install --user git+https://github.com/bitfinexcom/bfx-hf-indicators-py 
#  pip3.8 install --user python-binance
#
# Remember you are using this at your own risk, don't come crying to us if it fucks up your wallet. Thank you.
#==============================================================================================================#

import requests
import os
import time
import sys
import math
from datetime import datetime
from bfxhfindicators import sma
from secrets import *
from fuctions import *
from settingsbtc import *
from binance.client import Client

logging(3, 'BOT', 'Starting bot version ' + versio, 'Peep peep boop', 1)
client = Client(API_KEY, API_SECRET)

#flags to remember what is bought 
#lippu 1 for alts
lippu1 = []
#lippu 2 for stables
lippu2 = []


for signal in SIGNALS:
    tiedot.append({'symbol' : signal[0] , 'TIMEFRAME' : signal[1], 'SMA_PERIODS': [signal[2], signal[3]], 'LIMIT_NO': max([signal[2], signal[3]]), 'maara': signal[4], 'kolikko1': signal[5], 'kolikko2': signal[6], 'last_action': checkLastAction(signal[5], signal[4], signal[0], client), 'SMA_POINTS':[signal[7],signal[8]], 'sma1multip':signal[9], 'sma2multip':signal[10], 'tradeprice':0})
for y in tiedot:
    if y['last_action'] == 'BUY':
        lippu1.append(y['kolikko1'])
        lippu2.append(y['kolikko2'])

laskuri = 0
#loop until end of the world
while True:
    laskuri = laskuri + 1 
    if laskuri == 100:
        logging(3, tieto['symbol'],'Ping pong', 'Still alive and nothing to report', 1)
        laskuri = 0
    #Get BTC info for every round  
    parsed_klines = getCandles(BTCINFO[0], BTCINFO[1], max([BTCINFO[2], BTCINFO[3]]), client)  
    sma1 = sma.SMA(BTCINFO[2])
    sma2 = sma.SMA(BTCINFO[3])
    for kline in parsed_klines:
        sma1.add(kline[BTCINFO[6]])
        sma2.add(kline[BTCINFO[7]])  
    btcsma1 = sma1.v() 
    btcsma2 = sma2.v()
    if btcsma1 > btcsma2: btcaction = 'PUMP'
    else: btcaction = 'DUMP'
    
    #check if trendlines are set and set symbols in array for later check
    linjat = getLines()
    linjakolikot = []
    if linjat:
        for linja in linjat:
            linjakolikot.append(linja[0])
    print(linjakolikot)

    for tieto in tiedot:
        try:
            new_action = ''
            print(tieto['symbol'])
            #check if stable is already used for something else
            if tieto['kolikko2'] in lippu2 and not tieto['kolikko1'] in lippu1: continue
            
            hinta = float(getLastPrice(tieto['symbol'], client))

            #apply stoploss percentage, if not over/under stoploss, do not trade
            if (hinta < (STOPLOSS/100+1)*tieto['tradeprice']) and (hinta > (1-STOPLOSS/100)*tieto['tradeprice']): continue
            
            #check if there is trendlines for token/coin and check prices or go to normal sma functionality
            print(tieto['symbol'])
            if tieto['symbol'] in linjakolikot:
                print('Kolikko loytynyt linjoista')
                print(tieto['symbol'])
                for linja in linjat:
                    if tieto['symbol'] == linja[0]:
                        linjahinnat = getLineprices(linja)
                        print('linjahinnat')
                        print(linjahinnat)
                        print('hinta')
                        print(hinta)
                        if hinta > linjahinnat[1]:
                            new_action = 'BUY'
                            linjat.remove(linja)
                        elif hinta < linjahinnat[0]:
                            new_action = 'SELL'
                            linjat.remove(linja)
                        else: continue
                if new_action == '': continue
            else:
                #get candles, 1 = alt and 2 = btc  
                parsed_klines1 = getCandles(tieto['symbol'], tieto['TIMEFRAME'], tieto['LIMIT_NO'], client)
                parsed_klines2 = getCandles(tieto['symbol'], BTCINFO[1], tieto['LIMIT_NO'], client)
                
                #get sma values, 1 = alt and 2 = btc 
                sma1 = sma.SMA(tieto['SMA_PERIODS'][0])
                sma2 = sma.SMA(tieto['SMA_PERIODS'][1])
                sma3 = sma.SMA(tieto['SMA_PERIODS'][0])
                sma4 = sma.SMA(tieto['SMA_PERIODS'][1])      
                for kline in parsed_klines1:
                    sma1.add(kline[tieto['SMA_POINTS'][0]])
                    sma2.add(kline[tieto['SMA_POINTS'][1]])
                for kline in parsed_klines2:
                    sma3.add(kline[tieto['SMA_POINTS'][0]])
                    sma4.add(kline[tieto['SMA_POINTS'][1]])      
                smashort = sma1.v() > sma2.v()
                smalong = sma3.v() > sma4.v()
                
                

                #check if trade is needed and what we are doing, if BTC is going up we buy easier and if BTC dumps we sell easier
                
                if (tieto['last_action'] == 'BUY') and (btcaction == 'PUMP') and smashort == False and smalong == False: new_action = 'SELL' 
                elif tieto['last_action'] == 'SELL' and (btcaction == 'PUMP') and smashort == True: new_action = 'BUY' 
                elif tieto['last_action'] == 'BUY' and (btcaction == 'DUMP') and smashort == False: new_action = 'SELL'
                elif tieto['last_action'] == 'SELL' and (btcaction == 'DUMP') and smashort == True and smalong == True: new_action = 'BUY'
                else: continue

            
            
            #create trade clause
            kauppalause = ''
            kauppalause = "client.create_test_order(symbol='" + str(tieto['symbol']) + "',side='" + str(new_action) + "',type='" + str(tyyppi)
            if tieto['maara'] == 0 :
                if new_action == 'BUY':
                    balance = truncate(float(client.get_asset_balance(asset=tieto['kolikko2'])['free']) * 0.98, DECIMALS[tieto['kolikko2']])
                    kauppalause = kauppalause + "',quoteOrderQty=" + str(balance) +")"
                else:
                    balance = truncate(float(client.get_asset_balance(asset=tieto['kolikko1'])['free']),DECIMALS[tieto['kolikko1']])
                    kauppalause = kauppalause + "',quantity=" + str(balance)+")"
            else: kauppalause = kauppalause + "',quantity=" + str(tieto['maara'])+")"

            #do trade
            handleTrade(kauppalause, client, tieto)

            #set values for next loop
            tieto['tradeprice'] = hinta
            tieto['last_action'] = new_action
            if new_action == 'BUY':
                lippu1.append(tieto['kolikko1'])
                lippu2.append(tieto['kolikko2'])
            elif new_action == 'SELL':
                lippu1.remove(tieto['kolikko1'])
                lippu2.remove(tieto['kolikko2'])
            putLines(linjat)
                
        #handle exception
        except Exception as e:
            logging(2, tieto['symbol'], 'FAIL: ', str(e), 1)
            continue
        time.sleep(SLEEPTIME2)    
    time.sleep(SLEEPTIME)
    
