from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class PriceHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(100))
    price = db.Column(db.String(100))
    date = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, ticker, price, date=None):
        self.ticker = ticker
        self.price = price
        if date:
            self.date = date
        else:
            self.date = datetime.now()