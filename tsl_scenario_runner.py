import csv
import os
import glob
 
#https://www.binance.com/en/landing/data Download input files

#Setting the source directory for input files in current directory
path = os.path.join(os.path.dirname(__file__), "tsl_data")

try:

    for filename in glob.glob(os.path.join(path, '*.csv')):
        
        #parsering the coin-pair from the filename
        coin_pair = os.path.basename(filename).split('-')[0]
        if len(coin_pair) == 7:
            alt = coin_pair[0:3]
            stable = coin_pair[3:]
        else:
            alt = coin_pair[0:4]
            stable = coin_pair[4:]
            
        with open(os.path.join(os.getcwd(), filename), newline='') as csv_file:
            
            print("\nProcessing file: " + os.path.basename(filename))
            print("Alt coin: " + alt)
            print("Stable coin: " + stable)            
            
            for mplier in range(1,10):
                counter = 0
                buy_price = 0
                sell_price = 0
                buy_order = 0
                sell_order = 0
                fee_mplier = 0.998
                transaction = ""
                amount = 1000
                final_price = 0
                symbol = ""
                trade_counter = 0
             
                f = csv.reader(csv_file, delimiter=',')
                csv_file.seek(0)
                for i in f:

                    #set the initial price
                    if counter == 0:
                        buy_price = float(i[1])
                        sell_order = buy_price * (1 - mplier/100)
                        transaction = 'BOUGHT'
                        symbol = "ALT"
                        amount = amount / buy_price * fee_mplier
                        trade_counter += 1
            
                    else:
                        #if bought then compare the current price to sell_order
                        if transaction == 'BOUGHT':
                            #sell, if the current price lower than sell_order and set a new buy_order
                            if float(i[1]) <= sell_order:
                                sell_price = float(i[1])
                                amount = amount * sell_price * fee_mplier
                                buy_order = sell_price * (1 + mplier/100)
                                trade_counter += 1
                                transaction = "SOLD"
                                symbol = "BUSD"              
            
                            #don't sell, but set new sell_order which is higher than the previous one:
                            elif float(i[1]) > (sell_order * (1 + mplier/100)):    
                                sell_order = float(i[1]) * (1 - mplier/100)           
            
                        #if sold then compare current price to buy_order        
                        elif transaction == 'SOLD':
                            #buy, if the current price higher than sell order and set a new sell_order
                            if float(i[1]) >= buy_order:
                                buy_price = float(i[1])
                                amount = amount / buy_price * fee_mplier
                                sell_order = buy_price * (1 - mplier/100)
                                trade_counter += 1
                                transaction = "BOUGHT"
                                symbol = "ALT"             
            
                            #don't buy, but set new buy_order which is lower than the previous one
                            elif float(i[1]) <= (buy_order * (1 - mplier/100)):                        
                                buy_order = float(i[1]) * (1 + mplier/100)             
            
                    counter += 1     

                if symbol == "ALT":
                    amount = amount * float(i[1])
                    
                print(str(mplier) + '% : ' + str(int(amount)) + " " + stable + ". Trades made: " + str(trade_counter))
except NameError:
    print("Input file not found.")    