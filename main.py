from flask import Flask, render_template, request, redirect, url_for, g, session
import sqlite3
import requests
from bs4 import BeautifulSoup
from nsetools import Nse
import yfinance as yf


company_chart={
    'ITC':'https://app.powerbi.com/reportEmbed?reportId=9dc112d3-afe4-4237-88de-fc132517a070&autoAuth=true&ctid=56111054-529c-4d98-8a2b-43b0a0bbf946',
    'ZEEL':'https://app.powerbi.com/reportEmbed?reportId=34ff263c-926c-45b4-83c4-9bf174955a97&autoAuth=true&ctid=56111054-529c-4d98-8a2b-43b0a0bbf946',
     'WIPRO':'https://app.powerbi.com/reportEmbed?reportId=cab37571-3db4-4399-b1c0-69d04a63d8d5&autoAuth=true&ctid=56111054-529c-4d98-8a2b-43b0a0bbf946',
     'VEDL':'https://app.powerbi.com/reportEmbed?reportId=7d71b458-a8c5-43b2-bd1b-d2f02b271131&autoAuth=true&ctid=56111054-529c-4d98-8a2b-43b0a0bbf946',
     'UPL':'https://app.powerbi.com/reportEmbed?reportId=33459f21-9e12-4481-b419-ec8b4c82d336&autoAuth=true&ctid=56111054-529c-4d98-8a2b-43b0a0bbf946',
     'ULTRACEMCO':'https://app.powerbi.com/reportEmbed?reportId=1bbcb517-7153-4945-a439-47efbba2e89f&autoAuth=true&ctid=56111054-529c-4d98-8a2b-43b0a0bbf946',
     'TITAN':'https://app.powerbi.com/reportEmbed?reportId=4e3d73cb-dfc1-42f4-a22d-3fb929320747&autoAuth=true&ctid=56111054-529c-4d98-8a2b-43b0a0bbf946',
     'TECHM':'https://app.powerbi.com/reportEmbed?reportId=5f57a944-6c7e-4c6e-853c-8e432f9c95c8&autoAuth=true&ctid=56111054-529c-4d98-8a2b-43b0a0bbf946',
     'TCS':'https://app.powerbi.com/reportEmbed?reportId=8b35c521-5b22-42ab-8257-3dc24db08dc7&autoAuth=true&ctid=56111054-529c-4d98-8a2b-43b0a0bbf946',
     'TATASTEEL':'https://app.powerbi.com/reportEmbed?reportId=7171a25f-d7d3-40a3-8a9b-d9c184375323&autoAuth=true&ctid=56111054-529c-4d98-8a2b-43b0a0bbf946',
     'TATAMOTORS':'https://app.powerbi.com/reportEmbed?reportId=6c1f2447-249f-4517-a551-471eb66eb489&autoAuth=true&ctid=56111054-529c-4d98-8a2b-43b0a0bbf946',
     'SUNPHARMA':'https://app.powerbi.com/reportEmbed?reportId=ba6aed4b-a695-4d7e-9871-ca857fc0150b&autoAuth=true&ctid=56111054-529c-4d98-8a2b-43b0a0bbf946',
     'SHREECEM':'https://app.powerbi.com/reportEmbed?reportId=eeaf2b7f-bb4b-4571-9177-9ebde8c36a6e&autoAuth=true&ctid=56111054-529c-4d98-8a2b-43b0a0bbf946',
     'SBIN':'https://app.powerbi.com/reportEmbed?reportId=f2a2391f-912a-487d-b49c-5d4c469d2319&autoAuth=true&ctid=56111054-529c-4d98-8a2b-43b0a0bbf946',
     'RELIANCE':'https://app.powerbi.com/reportEmbed?reportId=392433da-d851-4a17-aa30-80110a0b9f00&autoAuth=true&ctid=56111054-529c-4d98-8a2b-43b0a0bbf946',
      'POWERGRID':'https://app.powerbi.com/reportEmbed?reportId=f5878c54-deb7-4c54-af88-b86d27521228&autoAuth=true&ctid=56111054-529c-4d98-8a2b-43b0a0bbf946',
      'ONGC':'https://app.powerbi.com/reportEmbed?reportId=19773143-0e98-4eeb-beb6-631ac22022dd&autoAuth=true&ctid=56111054-529c-4d98-8a2b-43b0a0bbf946',
      'NTPC':'https://app.powerbi.com/reportEmbed?reportId=f0dd3f6a-e3af-43e0-96aa-b99c83c97076&autoAuth=true&ctid=56111054-529c-4d98-8a2b-43b0a0bbf946',
      'NESTLEIND':'https://app.powerbi.com/reportEmbed?reportId=1037dd3e-9bc7-495b-9906-36886fbdb7c4&autoAuth=true&ctid=56111054-529c-4d98-8a2b-43b0a0bbf946',
      'MM':'https://app.powerbi.com/reportEmbed?reportId=d2b6f59f-e223-4ffa-bdc5-7edffe342ca1&autoAuth=true&ctid=56111054-529c-4d98-8a2b-43b0a0bbf946',
      'MARUTI':'https://app.powerbi.com/reportEmbed?reportId=503f494f-7757-4eec-94aa-7e7f6caf8a0c&autoAuth=true&ctid=56111054-529c-4d98-8a2b-43b0a0bbf946',
      'LT':'https://app.powerbi.com/reportEmbed?reportId=cfa5fde7-af77-4847-84bc-dccc34dd4335&autoAuth=true&ctid=56111054-529c-4d98-8a2b-43b0a0bbf946',
      'KOTAKBANK':'https://app.powerbi.com/reportEmbed?reportId=118bc4cc-e235-4ce6-bdad-797edb7bedd1&autoAuth=true&ctid=56111054-529c-4d98-8a2b-43b0a0bbf946',
      'JSWSTEEL':'https://app.powerbi.com/reportEmbed?reportId=a0b4ac64-ec06-45fe-8d54-131e7ca514a5&autoAuth=true&ctid=56111054-529c-4d98-8a2b-43b0a0bbf946',
      'INFY':'https://app.powerbi.com/reportEmbed?reportId=597cbacd-8a60-4c7d-8354-0366cc0e56af&autoAuth=true&ctid=56111054-529c-4d98-8a2b-43b0a0bbf946',
        'HCLTECH':'https://app.powerbi.com/reportEmbed?reportId=4e3df491-4fc3-41a1-9e0a-9faddfae77f1&autoAuth=true&ctid=56111054-529c-4d98-8a2b-43b0a0bbf946',
        'GRASIM':'https://app.powerbi.com/reportEmbed?reportId=f9f54ce9-a562-4aef-8616-1cc8bc203467&autoAuth=true&ctid=56111054-529c-4d98-8a2b-43b0a0bbf946',
        'GAIL':'https://app.powerbi.com/reportEmbed?reportId=24153336-ac40-4e9d-a110-49703612de23&autoAuth=true&ctid=56111054-529c-4d98-8a2b-43b0a0bbf946',
        'EICHERMOT':'https://app.powerbi.com/reportEmbed?reportId=b976ec80-7572-4aac-91b4-31f59ca444ae&autoAuth=true&ctid=56111054-529c-4d98-8a2b-43b0a0bbf946',
        'DRREDDY':'https://app.powerbi.com/reportEmbed?reportId=428bb0b3-e48c-4003-953f-062a179e0d00&autoAuth=true&ctid=56111054-529c-4d98-8a2b-43b0a0bbf946',
        'COALINDIA':'https://app.powerbi.com/reportEmbed?reportId=963d9916-7746-4a3b-807c-a6dbd3a2e4dd&autoAuth=true&ctid=56111054-529c-4d98-8a2b-43b0a0bbf946',
        'CIPLA':'https://app.powerbi.com/reportEmbed?reportId=3381c1f5-561d-42c6-8c94-b7449ccd0c3a&autoAuth=true&ctid=56111054-529c-4d98-8a2b-43b0a0bbf946',
        'BRITANNIA':'https://app.powerbi.com/reportEmbed?reportId=b86905d7-cb92-4f9f-8bde-dd0ce79e43cf&autoAuth=true&ctid=56111054-529c-4d98-8a2b-43b0a0bbf946',
        'BPCL':'https://app.powerbi.com/reportEmbed?reportId=2e4fba22-9e67-4153-bfe3-d87db9ab9472&autoAuth=true&ctid=56111054-529c-4d98-8a2b-43b0a0bbf946',
        'BHARTIARTL':'https://app.powerbi.com/reportEmbed?reportId=f9556537-7aed-46a1-9983-6cd7fb674e83&autoAuth=true&ctid=56111054-529c-4d98-8a2b-43b0a0bbf946',
        'BAJFINANCE':'https://app.powerbi.com/reportEmbed?reportId=1e57a4e9-ca00-4740-ae52-434209ec6248&autoAuth=true&ctid=56111054-529c-4d98-8a2b-43b0a0bbf946',
        'BAJAJFINSV':'https://app.powerbi.com/reportEmbed?reportId=a4139f69-fa06-4b25-8387-6630d8fecfe9&autoAuth=true&ctid=56111054-529c-4d98-8a2b-43b0a0bbf946',
        'BAJAJ-AUTO':'https://app.powerbi.com/reportEmbed?reportId=9b28a153-23a1-4883-9341-16218d0ef080&autoAuth=true&ctid=56111054-529c-4d98-8a2b-43b0a0bbf946',
        'AXISBANK':'https://app.powerbi.com/reportEmbed?reportId=b1cce5c3-8bcc-4f58-9099-418fe2b46810&autoAuth=true&ctid=56111054-529c-4d98-8a2b-43b0a0bbf946',
        'ASIANPAINT':'https://app.powerbi.com/reportEmbed?reportId=a1ffd088-0b30-4c04-8316-60413a5bf4ec&autoAuth=true&ctid=56111054-529c-4d98-8a2b-43b0a0bbf946',
        'ADANIPORTS':'https://app.powerbi.com/reportEmbed?reportId=daef1aed-6586-4d28-9a03-41ebc85f235b&autoAuth=true&ctid=56111054-529c-4d98-8a2b-43b0a0bbf946',
        'HDFCBANK':'https://app.powerbi.com/reportEmbed?reportId=d202167d-f541-4184-a682-4f85087673e5&autoAuth=true&ctid=56111054-529c-4d98-8a2b-43b0a0bbf946'
}


def ratios(stock_code):
    url = f'https://www.screener.in/company/{stock_code}/consolidated/'
    headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
    # Make a GET request to the URL
    response = requests.get(url,headers=headers)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table containing the cash flow data
    cash_flow_table = soup.find_all('table')[8]

    # Extract the headers from the table
    headers = [th.text.strip() for th in cash_flow_table.select('thead th')]

    # Extract the rows from the table
    rows = []
    for tr in cash_flow_table.select('tbody tr'):
        row = [td.text.strip() for td in tr.select('td')]
        rows.append(row)

    return headers,rows

def balance_sheet(stock_code):

    # Define the Screener.in URL to scrape
    url = 'https://www.screener.in/company/' + stock_code + '/consolidated/'
    headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
    # Make a GET request to the URL
    response = requests.get(url,headers=headers)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table containing the balance sheet data
    balance_sheet_table = soup.find_all('table')[6]
    year_headers = [th.text.strip().split(' ')[-1] for th in soup.select('th')[1:]]
    res=[]
    for i in year_headers:
        if i=='':
            break
        else:
            res.append(i)
    res.insert(0,'date')
    # Extract the rows from the table
    rows = balance_sheet_table.find_all('tr')

    return res,rows



def news_fetch():
    # URL of the page to be scraped
    url = "https://finance.yahoo.com/"
    headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
    # Send a request to access the page
    response = requests.get(url,headers=headers)

    # Parse HTML content using Beautiful Soup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all the news headlines
    news_headlines = soup.find_all("h3")
    n = []

    # Display the news headlines
    for headline in news_headlines:
        n.append(headline.text.strip())
    
    return n

#scraping the price of the stock
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


app = Flask(__name__)
app.secret_key = 'somesecretkey'

DATABASE = 'users.db'

stocks = ["ZEEL", "WIPRO", "VEDL", "UPL", "ULTRACEMCO", "TITAN", "TECHM", "TCS", "TATASTEEL", "TATAMOTORS", "SUNPHARMA",
          "SHREECEM", "SBIN", "RELIANCE", "POWERGRID", "ONGC", "NTPC", "NESTLEIND", "MM", "MARUTI", "LT", "KOTAKBANK", 
            "JSWSTEEL", "ITC", "INFRATEL" ,"HCLTECH", "GRASIM", "GAIL", "EICHERMOT", "DRREDDY", "COALINDIA", "CIPLA", "BRITANNIA", 
            "BPCL", "BHARTIARTL","BAJFINANCE", "BAJAJFINSV", "BAJAJ-AUTO", "AXISBANK", "ASIANPAINT", "ADANIPORTS","INFY","HDFCBANK"]

# Create a database connection
def get_db():
    if not hasattr(g, '_database'):
        g._database = sqlite3.connect(DATABASE)
    return g._database

# Create the users table if it does not exist
def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                         username TEXT UNIQUE NOT NULL, 
                         password TEXT NOT NULL)''')
        db.commit()
        cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="COMLIST"')
        table_exists = cursor.fetchone()
        if not table_exists:

            cursor.execute('''CREATE TABLE IF NOT EXISTS COMLIST(
                            NAME TEXT UNIQUE NOT NULL)''')  
            db.commit()
        
            cursor.executemany('''INSERT INTO COMLIST VALUES(?)''',((stocks[i],) for i in range(len(stocks)))) 
            db.commit()
        

@app.before_first_request
def create_tables():
    init_db()

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, '_database'):
        g._database.close()

@app.route('/')
def home():
    return render_template('home.html')

@app.route("/about")
def about():
	return render_template("about.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # check if password meets the requirements
        if len(password) < 8 or \
            not any(char.isupper() for char in password) or \
            not any(char.isdigit() for char in password) or \
            not any(char in "!@#$%^&*()_+-=[]{}|;':\"<>,.?/" for char in password):
                error_msg = "Password must be at least 8 characters long and contain at least one uppercase letter, one number, and one special character."
                return render_template('register.html', error_msg=error_msg)
        try:
            # Insert the user into the database
            db = get_db()
            cursor = db.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            db.commit()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            # User already exists
            return render_template('register.html', error='Username already taken')
    else:
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        if user is not None:
            session['username'] = username
            return redirect(url_for('search'))
        else:
            return render_template('login.html', error='Invalid username or password')
    else:
        return render_template('login.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    nse = Nse()
    top_gainers = nse.get_top_gainers()
    top_losers = nse.get_top_losers()

    # Fetch index values
    data = yf.download("^GSPC ^DJI ^IXIC", period="1d")

    # Extract the index values and group by index name
    indices = {}
    for column in data.columns:
        index_type = column[0]
        index_name = column[1].split('^')[-1]
        index_value = round(data[column][-1], 2)
        if index_name not in indices:
            indices[index_name] = {}
        indices[index_name][index_type] = index_value


    if request.method == 'POST':
        name = request.form['search']
        name=name.upper()
        if name in stocks:
            return redirect(url_for('stock', name=name))
        else:
            return render_template('search.html', error='Company not found',top_gainers=top_gainers,top_losers=top_losers, indices=indices)
    else:
        return render_template('search.html',top_gainers=top_gainers,top_losers=top_losers,indices=indices)

@app.route('/stock/<name>')
def stock(name):
    if name in stocks:
        lp,cp,op,dl,dh=real_time_stock_fetch(name)
        n=news_fetch()
        res,rows=balance_sheet(name)
        h,r=ratios(name)
        print(company_chart[name])
        return render_template('stock.html', name=name,lp=lp,cp=cp,op=op,dl=dl,dh=dh,headlines=n,headers=res, rows=rows,h=h,r=r,chart_link=str(company_chart[name]))
    else:
        return render_template('search.html', error='Company not found')
        
@app.route('/logout' ,methods=['GET','POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)