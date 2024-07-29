import React, { useState, useEffect, useCallback } from 'react';
import Caret from './supportingJSX/Caret.jsx';

  const PriceTable = () => {
    const [prices, setPrices] = useState([]);
    const [sort, setSort] = useState({keyToSort: "date", direction: "dsc"});
    
    // Key is the same thing as accessor in the video 

    const headers = [
      { label: "Date", KEY: "date" },
      { label: "Ticker", KEY: "ticker" },
      { label: "Price", KEY: "price" },
      { label: "$ Change", KEY: "dollarChange" },
      { label: "% Change", KEY: "percentChange" },
     ];

     function handleHeaderClick(header){
      setSort({
        keyToSort: header.KEY,
        direction: header.KEY === sort.keyToSort ? sort.direction === "asc" ? "desc" : "asc" : "desc",
      });
     }
    
      const getSortedArray = (arrayToSort) => {
        const { keyToSort, direction } = sort;
        const sortedArray = [...arrayToSort].sort((a, b) => {
          let aValue = a[keyToSort];
          let bValue = b[keyToSort];
    
          // Handle date sorting
          if (keyToSort === "date") {
            aValue = new Date(aValue);
            bValue = new Date(bValue);
          }
    
          // Handle numeric sorting
          if (keyToSort === "price" || keyToSort === "dollarChange" || keyToSort === "percentChange") {
            aValue = parseFloat(aValue.replace(/[^0-9.-]+/g,"")); // Remove $ and % symbols and convert to number
            bValue = parseFloat(bValue.replace(/[^0-9.-]+/g,""));
          }
    
          if (aValue === null) return 1;
          if (bValue === null) return -1;
          if (aValue === null && bValue === null) return 0;
    
          if (direction === "asc") {
            return aValue > bValue ? 1 : -1;
          } else {
            return aValue > bValue ? -1 : 1;
          }
        });
    
        return sortedArray;
      };
  
    const fetchPrices = useCallback(async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/prices');
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        console.log('Fetched data:', data);
        return data;
      } catch (error) {
        console.error('Error fetching data:', error);
        return []; // Return an empty array on error
      }
    }, []);
  
    const fetchPreviousPrice = useCallback(async (ticker, id) => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/get_ticker_previous/${ticker}/${id}`);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const prevData = await response.json();
        console.log('Previous data:', prevData);
        return prevData;
      } catch (error) {
        console.error('Error fetching previous data:', error);
        return null; // Return null on error
      }
    }, []);
  
    const fetchPreviousPrices = useCallback(async (prices) => {
      try {
        const updatedPrices = await Promise.all(
          prices.map(async (item) => {
            const prevData = await fetchPreviousPrice(item.ticker, item.id);
            if (prevData) {
              const dollarChange = item.price - prevData.price;
              const percentChange = ((item.price - prevData.price) / prevData.price) * 100;
              return {
                ...item,
                dollarChange: '$' + dollarChange.toFixed(2),
                percentChange: percentChange.toFixed(2) + '%',
              };
            } else {
              return {
                ...item,
                dollarChange: '$0.00',
                percentChange: '0.00%',
              };
            }
          })
        );
        return updatedPrices;
      } catch (error) {
        console.error('Error processing previous prices:', error);
        return []; // Return an empty array on error
      }
    }, [fetchPreviousPrice]);
  
    useEffect(() => {
      const fetchData = async () => {
        const currentPrices = await fetchPrices();
        const updatedPrices = await fetchPreviousPrices(currentPrices);
        setPrices(updatedPrices);
      };
  
      fetchData();
    }, [fetchPrices, fetchPreviousPrices]);
/*
          <th>Date <span>&#9650;</span></th>
          <th>Ticker</th>
          <th>Price</th>
          <th>$ Change</th>
          <th>% Change</th>


                <span>
                <Caret direction={sort.keyToSort === label.KEY ? sort.direction : "adc"}/>
               </span>
*/
  return (
    <div className="table-container">
      <h2 className="heading">10 Most Recent Scrapes</h2>
      <table className="price-table">
        <thead>
          <tr>
            {headers.map((label, accessor) => (
              <th key = {accessor} onClick ={() => handleHeaderClick(label)}>
               <span>{label.label}</span>
                {label.KEY ===  sort.keyToSort && (
                <Caret 
                direction={sort.keyToSort === label.KEY ? sort.direction : "asc"}
                />  
                )}
              </th>
            )
            )}

          </tr>
        </thead>
        <tbody>
          {(getSortedArray(prices).slice(-10)).map((price, index) => (
            <tr key={price.id}>
              <td>{price.date}</td>
              <td>{price.ticker}</td>
              <td>{price.price}</td>
              <td>{price.dollarChange}</td>
              <td>{price.percentChange}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
/*
          {prices.slice(0, 10).map(price => (
            <tr key={price.id}>
              <td>{price.date}</td>
              <td>{price.ticker}</td>
              <td>{price.price}</td>
              <td>{price.dollarChange}</td>
              <td>{price.percentChange}</td>
            </tr>
          ))}
*/
export default PriceTable;
