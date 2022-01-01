import csv
import os
import glob
 
#https://www.binance.com/en/landing/data
rel_path = "tsl_data" #assuming that there is a folder "tsl_data" in current directory
path = os.path.join(os.path.dirname(__file__), rel_path)

try:

<<<<<<< HEAD
    for filename in glob.glob(os.path.join(path, '*.csv')):
        with open(os.path.join(os.getcwd(), filename), newline='') as csv_file:
            print("\nProcessing file: " + str(filename))
            for mplier in range(1,3):
                counter = 0
                buy_price = 0
                sell_price = 0
                buy_order = 0
                sell_order = 0
                fee_mplier = 0.998
                check_price = 0
                transaction = ""
                amount = 1000
                final_price = 0
                symbol = ""
                trade_counter = 0
                print(mplier, counter)
                
=======
    for mplier in range(1,20):
        counter = 0
        buy_price = 0
        sell_price = 0
        buy_order = 0
        sell_order = 0
        feekerroin = 0.998
        #mplier = 1 #change this to test different percentages
        check_price = 0
        transaction = ""
        amount = 1000
        final_price = 0
        symbol = ""        
        with open('AVAXUSDT-trades-2021-11.csv', newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            
            for i in csv_reader:
                #set the initial price
                #print(', '.join(i))
                if counter == 0:
                    buy_price = float(i[1])
                    sell_order = buy_price * (1 - mplier/100)
                    #print(sell_order)
                    transaction = 'BOUGHT'
                    symbol = "ALT"
                    amount = amount / buy_price * feekerroin
                    #print("Initial amount: " + str(amount) + " " + symbol)         
        
                else:         
        
                    #if bought then compare the current price to sell_order
                    if transaction == 'BOUGHT':
                        #sell, if the current price lower than sell_order and set a new buy_order
                        if float(i[1]) <= sell_order:
                            sell_price = float(i[1])
                            amount = amount * sell_price * feekerroin
                            buy_order = sell_price * (1 + mplier/100)
                            #print("Trade made! Sold " + str(amount/sell_price) + " " + symbol + " in " + str(sell_price))
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
                            amount = amount / buy_price * feekerroin
                            sell_order = buy_price * (1 - mplier/100)
                            transaction = "BOUGHT"
                            symbol = "ALT"
                            #print("Trade made! Bought " + str(amount) + " " + symbol + " in " + str(sell_price))              
        
                        #don't buy, but set new buy_order which is lower than the previous one
                        elif float(i[1]) <= (buy_order * (1 - mplier/100)):                        
                            buy_order = float(i[1]) * (1 + mplier/100)
             
        
                counter = counter + 1     
>>>>>>> 70d38088b0c23f5d728886e6312359df19c1849e
        
        #with open('FTMBUSD-trades-2021-12-30.csv', newline='') as csv_file:
        #    csv_reader = csv.reader(csv_file, delimiter=',')
        #for filename in glob.glob(os.path.join(path, '*.csv')):
           # with open(os.path.join(os.getcwd(), filename), newline='') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for i in csv_reader:
                    #print(mplier, counter)
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
            
                print(str(mplier) + '% : ' + str(int(amount)) + " Trades made: " + str(trade_counter))
except NameError:
    print("Input file not found.")    