from datetime import datetime


def getLines():
    lines = open('trendlines.txt','r').readlines()
    if not lines: return 0
    linjat=[]
    for line in lines:
        line = line.replace('\n','')
        line = line.replace('[','')
        line = line.replace(']','')
        line = line.replace(' ','')
        line = line.replace("'","")   
        line = line.split(',')
        line[1] = int(line[1])
        line[3] = int(line[3])
        line[5] = int(line[5])
        line[7] = int(line[7])
        line[2] = int(datetime.timestamp(datetime.strptime(str(line[2]),"%d.%m.%Y")))
        line[4] = int(datetime.timestamp(datetime.strptime(str(line[4]),"%d.%m.%Y")))
        line[6] = int(datetime.timestamp(datetime.strptime(str(line[6]),"%d.%m.%Y")))
        line[8] = int(datetime.timestamp(datetime.strptime(str(line[8]),"%d.%m.%Y")))
        linjat.append(line)
    return linjat

def putLines(linjat):
    filu = open('trendlines.txt','w')
    filu.close()
    if not linjat: return 0
    filu = open('trendlines.txt','a')
    for iteration, linja in enumerate(linjat):
        linjat[iteration][2] = datetime.fromtimestamp(int(linjat[iteration][2])).strftime('%d.%m.%Y')
        linjat[iteration][4] = datetime.fromtimestamp(int(linjat[iteration][4])).strftime('%d.%m.%Y')
        linjat[iteration][6] = datetime.fromtimestamp(int(linjat[iteration][6])).strftime('%d.%m.%Y')
        linjat[iteration][8] = datetime.fromtimestamp(int(linjat[iteration][8])).strftime('%d.%m.%Y') 
        linjat[iteration] = str(linja) + '\n'
        linjat[iteration] = linjat[iteration].replace(']','')
        linjat[iteration] = linjat[iteration].replace('[','')
        linjat[iteration] = linjat[iteration].replace(' ','')
    linjat[-1] = linjat[-1].replace('\n','')
    for linja in linjat:
        filu.write(str(linja))
    filu.close()
    return 1
# price, day
# yhtalo: y = kx + b
# k = kulmakerroin
#	dy / dx = k
# y = y-koordinaatti eli hinta
# x = x-koordinaatti eli aika
# b = kohta missa ylittaa y-akselin, x ollessa 0
linjat = getLines()
print(linjat)

now = datetime.timestamp(datetime.now())
print('NOW:')
print(now)
#lower line
#[['FTMUSDT', 38611, 1632862800, 55633, 1633899600, 45770, 1632862800, 63463, 1633899600], ['ROSEUSDT', 38611, 1632862800, 55633, 1633899600, 45770, 1632862800, 63463, 1633899600]]

date1 = int(linjat[0][2])
date2 = int(linjat[0][4])
dx = date2 - date1 
dy = linjat[0][3]-linjat[0][1]
k = dy/dx
b = linjat[0][1] -(k*date1)
b2 = linjat[0][3] -(k*date2)
print('viiva1 nyt')
v1nyt = k*now+b
print(v1nyt)
date1 = int(linjat[0][6])
date2 = int(linjat[0][8])
dx = date2 - date1 
dy = linjat[0][7]-linjat[0][5]
k = dy/dx
b = linjat[0][5] -(k*date1)
b2 = linjat[0][7] -(k*date2)
print('viiva2 nyt')
v2nyt = k*now+b
print(v2nyt)

#putLines(linjat)



