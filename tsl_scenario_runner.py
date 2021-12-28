import csv
import glob
 
#https://www.binance.com/en/landing/data
try:
    counter = 0
    buy_price = 0
    sell_price = 0
    buy_order = 0
    sell_order = 0
    mplier = 3 #change this to test different percentages
    check_price = 0
    transaction = ""
    amount = 1000
    final_price = 0
    symbol = ""
    
    with open('FTMBUSD-trades-2021-12-25.csv', newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        
        for i in csv_reader:
            #set the initial price
            #print(', '.join(i))
            if counter == 0:
                buy_price = float(i[1])
                sell_order = buy_price * (1 - mplier/100)
                print(sell_order)
                transaction = 'BOUGHT'
                symbol = "ALT"
                amount = amount / buy_price
                print("Initial amount: " + str(amount) + " " + symbol)         
    
            else:         
    
                #if bought then compare the current price to sell_order
                if transaction == 'BOUGHT':
                    #sell, if the current price lower than sell_order and set a new buy_order
                    if float(i[1]) <= sell_order:
                        sell_price = float(i[1])
                        amount = amount * sell_price
                        buy_order = sell_price * (1 + mplier/100)
                        print("Trade made! Sold " + str(amount/sell_price) + " " + symbol + " in " + str(sell_price))
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
                        amount = amount / buy_price
                        sell_order = buy_price * (1 - mplier/100)
                        transaction = "BOUGHT"
                        symbol = "ALT"
                        print("Trade made! Bought " + str(amount) + " " + symbol + " in " + str(sell_price))              
    
                    #don't buy, but set new buy_order which is lower than the previous one
                    elif float(i[1]) <= (buy_order * (1 - mplier/100)):                        
                        buy_order = float(i[1]) * (1 + mplier/100)
         
    
            counter = counter + 1     
    
        print(amount)
    
        if symbol == "ALT":
            amount = amount * float(i[1]) 
    
        print("Final amount: " + str(amount) + " BUSD")
        print(str(counter) + " rows processed.")

except:
    print("Input file not found.")    