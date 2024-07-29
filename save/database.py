from flask import Flask, jsonify, request, url_for, redirect, render_template, flash
from flask_cors import CORS
from bs4 import BeautifulSoup
import requests, json
from flask_sqlalchemy import SQLAlchemy
from models.users import db, PriceHistory

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
        url_complete_google = "https://www.google.com/finance/quote/NKLA:NASDAQ" 

        #get the ticker from user input
        ticker = request.form["addBox"]
        url_complete_yahoo = f"https://finance.yahoo.com/quote/{ticker}/"
        try:
            result = requests.get(url_complete_yahoo)

            # error handling if the ticker does not exist
            if result.status_code == 404:
                flash("Ticker not found, please try again.")
                return redirect(url_for('get_data', worked = False))
            
            picture = BeautifulSoup(result.content, 'html.parser')

            # filter for ticker and price
            price_element = picture.find('fin-streamer', {
                'data-field': 'regularMarketPrice',
                'data-testid': 'qsp-price'
            })

            if price_element:
                print(price_element['data-value'])
                print(price_element['data-symbol'])
                #span_tag = price_element.find('span')
                #price_text = f"${span_tag.get_text()}"

                new_price = PriceHistory(
                    price=price_element['data-value'],
                    ticker=price_element['data-symbol'],
                )
                db.session.add(new_price)
                db.session.commit()
                flash(f"{ticker} was added successfully.")
                return redirect(url_for('get_data', worked = True))
                #return jsonify({"Price": price_element['data-value'], 'Ticker': price_element['data-symbol'] })
                # NEED TO WORK ON FLASHING THIS IS THE HIGH PRIO THING RIGHT NOW FIX THIS RESUME HERE -----------------------------------
                # make it work/ integrate to the UI so that people know that the thing is happening.
            else:
                return redirect(url_for('get_data', worked = False))
            
        

        except requests.exceptions.RequestException as e:
            # Handle network-related errors
            flash(f"Request failed: {e}")
            return redirect(url_for('get_data'), False)
    else:
        return redirect(url_for('get_data'))


    # Find the price element
    # FOR YAHOO FINANCE
    

    
    


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
    prices = PriceHistory.query.all()
    return jsonify([{
        'id': price.id,
        'ticker': price.ticker,
        'price': price.price,
        'date' : price.date,
    } for price in prices])

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

if __name__ == '__main__':
    # Initialize the database
    with app.app_context():
        db.create_all()
    app.run(debug=True)

