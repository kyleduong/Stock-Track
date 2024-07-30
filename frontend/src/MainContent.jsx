import React, { useState, useEffect  } from 'react';
import {fetchTickers} from './supportingJSX/tickers.jsx';
import './styles.css';
import axios from 'axios'; 

const MainContent = ({ showImage, scrapAlert }) => {
const [searchTerm, setSearchTerm] = useState('');
const [addTerm, setAddTerm] = useState('');
const [message, setMessage] = useState('');
const [data, setData] = useState([]);

useEffect(() => {
  const loadTickers = async () => {
    const tickers = await fetchTickers();
    setData(tickers);
  };
  loadTickers();
}, []);

const handleScrap = async () => {
  try {
    const response = await axios.post('http://localhost:5000/scrape_price', { ticker: addTerm });
    setMessage(response.data.message);
    console.log("Price:", response.data.price);
    setAddTerm('')
    handleRefresh()
  } catch (error) {
    setMessage(error.response ? error.response.data.error : 'An error occurred');
  }
};

const handleSearch = (e) => {
  e.preventDefault(); // Prevent default form submission
  showImage(searchTerm.toLowerCase());
};

const scraperAlert = (e) => {
  e.preventDefault(); // Prevent default form submission
  scrapAlert(addTerm);
};

const handleRefresh = () => {
  window.location.reload();  // Refresh the page
};

console.log(addTerm)

return (
  <>
  <div className="left">
    <h2 className="centered-header">Price history</h2>
    <div className="scrollable-box">
        <ul>
            {data.filter((item) => {
              return searchTerm.toLowerCase() === '' ? item : item.toLowerCase().includes(searchTerm.toLowerCase())
            })
            .map(item => (
            <li key={item}>
                <div onClick={() => showImage(item)}>{item}</div>
            </li>
            ))}
        </ul>
    </div>
  </div>

  <div className="right">
    <div className="search-container">
      <form action="/" method = "POST" onSubmit={scraperAlert}>
        <h1 className="heading-search">Search for an existing ticker</h1>
        <input
          type="text"
          name="searchBox"
          placeholder="Search..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <button type="submit">Search</button>
      </form>

      <form onSubmit={(e) => { e.preventDefault(); handleScrap();}}>
        <h1 className="heading">Scrape Stock to the Database</h1>
        <input
          type="text"
          name="addBox"
          placeholder="Add ticker here..."
          value={addTerm}
          onChange={(e) => setAddTerm(e.target.value)}
        />
        <button type="submit" >Scrape!</button>
      </form>

      <div id="flash-messages">
        {message}
      </div>
    </div>
  </div>

</>
);
};


export default MainContent;
