from flask import Flask, jsonify, request, url_for, redirect, render_template, flash
from flask_cors import CORS
from bs4 import BeautifulSoup
import requests, json
from flask_sqlalchemy import SQLAlchemy
from models import db, PriceHistory
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
CORS(app)


db.init_app(app)

# Define a route to fetch data
@app.route('/', methods=['GET', 'POST'])
def get_data(worked=None):
    if request.method == "POST":
        user = request.form["searchBox"]
        return redirect(url_for("user", usr = user))
    else:
        return render_template("index.html")

@app.route("/api/<usr>", methods=['GET'])
def user(usr):
    return f"<h1>{usr}</h1>"


@app.route('/get_image_url')
def get_image_url():
    url = "https://www.newegg.com/asus-geforce-rtx-4070-ti-super-tuf-rtx4070tis-o16g-gaming/p/N82E16814126685"
    result = requests.get(url)
    picture = BeautifulSoup(result.content, 'html.parser')

    # Find the image element
    image_element = picture.find('img', {'class': 'product-view-img-original'})

    # Get the image URL
    image_url = image_element['src']
    return jsonify({"image_url": image_url})

# first scrapper
@app.route('/find_price')
def find_price():
    url = "https://www.newegg.com/asus-geforce-rtx-4070-ti-super-tuf-rtx4070tis-o16g-gaming/p/N82E16814126685"
    result = requests.get(url)
    picture = BeautifulSoup(result.content, 'html.parser')

    # Find the price element
    price_element = picture.find('li', {'class': 'price-current'})

    if price_element:
        # Extract the text from the <strong> and <sup> tags

        strong_tag = price_element.find('strong')
        sup_tag = price_element.find('sup')

        if strong_tag and sup_tag:
            # Combine the text to form the full price
            price_text = f"${strong_tag.get_text()}{sup_tag.get_text()}"
        else:
            price_text = "Price not found"
    else:
        price_text = "Price not found"

    return jsonify({"Price": price_text})

# the route/function that is going to be used in the timely calls
# RESUME HERE --------------------------------------------------------------------------
# what is left to do here, you will scrap the yahoo page, so figure out the prices and hmtl attributes to scrape
# then link it to the button, where clicking it will scrape once, getting the price of the stock and logging it to the database.
# once ur done with that, we have to figure out how to display/read the db information and show it, preferably on a graph but rn it can be just in a text box

#SECOND THOUGHT: get the ticker through a request. You can use /ticker/ in url for something you will link to from the fetch and it will show graph?
@app.route('/scrape_price', methods = ['POST'])
def scrape_price():

    if request.method == 'POST':

        #get the ticker from user input
        ticker = request.json.get("ticker")
        url_complete_yahoo = f"https://finance.yahoo.com/quote/{ticker}/"
        try:
            result = requests.get(url_complete_yahoo)

            # error handling if the ticker does not exist
            if result.status_code == 404:
                flash("Ticker not found, please try again.")
                return jsonify({"error": "Ticker not found"}), 404
            
            picture = BeautifulSoup(result.content, 'html.parser')

            # filter for ticker and price
            price_element = picture.find('fin-streamer', {
                'data-field': 'regularMarketPrice',
                'data-testid': 'qsp-price'
            })

            if price_element:
                print(price_element['data-value'])
                print(price_element['data-symbol'])

                new_price = PriceHistory(
                    price=price_element['data-value'],
                    ticker=price_element['data-symbol'],
                )
                db.session.add(new_price)
                db.session.commit()
                flash(f"{ticker} was added successfully.")
                return jsonify({"message": f"{ticker} was added successfully.", "price": price_element['data-value']}), 200
            else:
                return jsonify({"error": "Price element not found"}), 500
            
        except requests.exceptions.RequestException as e:
            # Handle network-related errors
            flash(f"Request failed: {e}")
            return jsonify({"error": str(e)}), 500


# click on the add button and input json to add to database
@app.route('/add', methods=['GET', 'POST'])
def add_price():
    if request.method == "POST":
        
        data = request.form["addBox"]  # Get raw data as text
        print(data)
        try:
            json_data = json.loads(data)  # Parse JSON data
        except json.JSONDecodeError:
            return jsonify({"error": "Invalid JSON data",}), 400
        new_price = PriceHistory(
            ticker=json_data['ticker'],
            price=json_data['price'],
        )
        db.session.add(new_price)
        db.session.commit()
        return jsonify({"message": "Price added successfully"}), 201
    else:
        return render_template("index.html")
    
# read an object's ticker
@app.route('/get_ticker/<tickr>', methods=['GET'])
def get_ticker(tickr):
    ticker = PriceHistory.query.filter_by(ticker=tickr).first()
    
    if ticker is None:
        # Return a 404 error if the item is not found
        return jsonify({'error': 'Item not found'}), 404
    return jsonify({
        'id': ticker.id,
        'ticker': ticker.ticker,
        'price': ticker.price,
        'date': ticker.date,
    })


# read an object's price
@app.route('/get_price/<int:id>', methods=['GET'])
def get_price(id):
    stocks = PriceHistory.query.get(id)
    return jsonify([{
        'id': price.id,
        'ticker': price.ticker,
        'price': price.price,
        'date' : price.date,
    } for price in stocks])

# read an object's date read
@app.route('/get_date/<int:id>', methods=['GET'])
def get_date(id):
    stocks = PriceHistory.query.all()
    return jsonify([{
        'id': price.id,
        'ticker': price.ticker,
        'price': price.price,
        'date' : price.date,
    } for price in stocks])

# reads all of the database objects
@app.route('/prices', methods=['GET'])
def get__all_prices():
    prices = PriceHistory.query.order_by(PriceHistory.id.desc()).all()
    return jsonify([{
        'id': price.id,
        'ticker': price.ticker,
        'price': price.price,
        'date' : price.date,
    } for price in prices])

# reads database object with given id
@app.route('/prices/<int:ids>', methods=['GET'])
def get_price_id(ids):
    ticker = PriceHistory.query.filter(
        PriceHistory.id == ids
        )
    if ticker is None:
        # Return a 404 error if the item is not found
        return jsonify({'error': 'Item not found'}), 404
    return jsonify([{
        'id': ticker.id,
        'ticker': ticker.ticker,
        'price': ticker.price,
        'date' : ticker.date,
    }])

# update the databse objects
@app.route('/update/<int:id>', methods=['PUT'])
def update_price(id):
    data = request.get_json()
    price = PriceHistory.query.get_or_404(id)
    price.ticker = data['ticker']
    price.price = data['price']
    db.session.commit()
    return jsonify({"message": "Price updated successfully"})

# delete a database object with given id
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_price(id):
    price = PriceHistory.query.get_or_404(id)
    db.session.delete(price)
    db.session.commit()
    return jsonify({"message": "Price deleted successfully"})

# read an object's ticker
# done by getting the ticker, and its id, and returning the object with the next greatest id.
@app.route('/get_ticker_previous/<tickr>/<int:id>', methods=['GET'])
def get_ticker_previous(tickr, id):
    ticker = PriceHistory.query.filter(
        PriceHistory.ticker == tickr,
        PriceHistory.id < id
    ).order_by(PriceHistory.id.desc()).first()
    
    if ticker is None:
        # Return a 404 error if the item is not found
        return jsonify({'error': 'Item not found'}), 404
    return jsonify({
        'id': ticker.id,
        'ticker': ticker.ticker,
        'price': ticker.price,
        'date': ticker.date,
    })

# get all of the objects that belong to a certain ticker
@app.route('/get_all_ticker/<tickr>', methods=['GET'])
def get_all_ticker(tickr):
    tickers = PriceHistory.query.filter_by(ticker=tickr).all()
    
    if tickers is None:
        # Return a 404 error if the item is not found
        return jsonify({'error': 'Item not found'}), 404
    
    result = []
    for ticker in tickers:
        result.append({
            'id': ticker.id,
            'ticker': ticker.ticker,
            'price': ticker.price,
            'date': ticker.date,
        })

    return result

# PURELY FOR SCHEDULER ---------------------------------------------------------------------------------------

# return all of the tickers in the database
@app.route('/get_all_tickers_in_database/', methods=['GET'])
def get_all_ticker_in_database():
    tickers = PriceHistory.query.all()
    
    if tickers is None:
        # Return a 404 error if the item is not found
        return jsonify({'error': 'Item not found'}), 404
    
    result = []
    for ticker in tickers:
        if ticker.ticker not in result:
            result.append(ticker.ticker)

    return result

# fetch the ticker data without all of the printing or returning
def fetch_ticker_data(ticker):
    with app.app_context():
        url_complete_yahoo = f"https://finance.yahoo.com/quote/{ticker}/"
        try:
            result = requests.get(url_complete_yahoo)
            if result.status_code == 404:
                print(f"Ticker {ticker} not found.")
                return None

            picture = BeautifulSoup(result.content, 'html.parser')
            price_element = picture.find('fin-streamer', {
                'data-field': 'regularMarketPrice',
                'data-testid': 'qsp-price'
            })

            if price_element:
                print(price_element['data-value'])
                print(price_element['data-symbol'])

                new_price = PriceHistory(
                    price=price_element['data-value'],
                    ticker=price_element['data-symbol'],
                )
                db.session.add(new_price)
                db.session.commit()
                print(f"Scraped and saved data for {ticker}")
            else:
                print(f"Price element not found for ticker {ticker}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed for ticker {ticker}: {e}")

# scrapes all of the tickers
def scrape_all_tickers():
    with app.app_context():
        tickers = get_all_ticker_in_database()  # function call, gets all tickers in database
        for ticker in tickers:
            fetch_ticker_data(ticker)

# scheduler, runs code in intervals while the servers are up
scheduler = BackgroundScheduler()
scheduler.add_job(func=scrape_all_tickers, trigger="interval", minutes=1)
#scheduler.start()

# Shut down the scheduler when exiting the app
#atexit.register(lambda: scheduler.shutdown())



if __name__ == '__main__':
    # Initialize the database
    with app.app_context():
        db.create_all()
    app.run(debug=True)

