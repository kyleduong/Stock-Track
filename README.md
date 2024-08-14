# Stock Webscraper

This project is a stock tracking application that features a React frontend and a Flask backend. It allows users to search for and monitor various stocks, view their history, and visualize stock data with graphs.

## Features

- **Stock Tracking:** Keeps track of selected stocks in a PostgreSQL database.
- **Search Functionality:** Search for stocks using the integrated search bar.
- **Scrollable History:** View a scrollable box containing the history of tracked stocks.
- **Graphical Visualization:** Displays graphs for each stock, showing historical data.

## Technologies Used

- **Frontend:** React.js
- **Backend:** Flask
- **Database:** PostgreSQL
- **Web Scraping:** BeautifulSoup, Requests
- **Graphing:** Chart.js

## Installation and Run

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/stock-webscraper.git
2. ** Install dependencies:**
   ```bash
   pip install -r requirements.txt
4. **Run files**
   ```bash
   run app.py
   cd frontend
   npm run dev

## Instructions

The code will run a scrape every second, scraping the prices of the stocks already in the database. Use the top search bar to filter through the list of stocks already in the database and view them individually. Use the bottom search bar to scrape a new stock to the database.

The table is used to display and filter through recent scrapes to the database. Filter and click on a stock to see a graph of the prices' history, allowing for you to analyze its data.
   
