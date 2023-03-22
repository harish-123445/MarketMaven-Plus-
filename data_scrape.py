import sys
import requests
from bs4 import BeautifulSoup
import re
import os

def real_time_stock_fetch(stock_code):
    stock_url='https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol='+str(stock_code)
    #print(stock_url)
    headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
    
    response=requests.get(stock_url,headers=headers)
    soup=BeautifulSoup(response.text,'html.parser')
    data=soup.find(id='responseDiv').getText().strip().split(":")
    #print(data)
    
    for item in data:
        if 'lastPrice' in item :
            index=data.index(item)+1
            latestprice=data[index].split('"')[1]
            lp=float(latestprice.replace(',',""))
        elif 'closePrice' in item :
            index=data.index(item)+1
            closeprice=data[index].split('"')[1]
            cp=float(closeprice.replace(',',""))
        elif 'open' in item :
            index=data.index(item)+1
            openprice=data[index].split('"')[1]
            op=float(openprice.replace(',',""))
        elif 'dayLow' in item :
            index=data.index(item)+1
            daylow=data[index].split('"')[1]
            dl=float(daylow.replace(',',""))
        elif 'dayHigh' in item :
            index=data.index(item)+1
            dayhigh=data[index].split('"')[1]
            dh=float(dayhigh.replace(',',""))
            
    return lp,cp,op,dl,dh
        
'''#for Mahindra & Mahindra company url if we use & symbol for stock_code it is actaully wrong ,stock code will be like M%26M,hence 
#we use regex for finding the pattern

regexp = re.compile('&')
stock_code='TATAPOWER'
OP  = []
LP  = []
DHP = []
DLP = []
CP  = []

os.system('cls')
print("--------------------------------------------------------------------------------------------------------------------------------------------")
print("|{:30s} | {:20s} | {:10s} | {:10s} | {:10s} | {:10s} | {:10s}|".format( 'Company Name','Symbol','openPrice','lastPrice','dayHigh','dayLow','closePrice'))
print("--------------------------------------------------------------------------------------------------------------------------------------------")

n=0
while n<50:
    n+=1
    try:
        if(regexp.search(stock_code) != None):
            stock_code = stock_code.replace('&','%26')
            
        lPrice,cPrice,oPrice, dlPrice, dhPrice= real_time_stock_fetch(stock_code)
    
        OP.append(str(oPrice))
        LP.append(str(lPrice))
        DHP.append(str(dhPrice))
        DLP.append(str(dlPrice))
        CP.append(str(cPrice))
         
        print("|{:30s} | {:20s} | {:10s} |{:10s} | {:10s} | {:10s} | {:10s} |".format((stock_code.lower()).capitalize(),stock_code,str(oPrice).rjust(10) , str(lPrice).rjust(10), str(dhPrice).rjust(10), str(dlPrice).rjust(10), str(cPrice).rjust(10)))
         
        print("--------------------------------------------------------------------------------------------------------------------------------------------")

    except KeyboardInterrupt:
        sys.exit()'''