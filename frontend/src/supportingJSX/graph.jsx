import React, { useState, useEffect, useCallback } from "react";
import { Line } from "react-chartjs-2";
import 'chart.js/auto';

const Graph = ({ticker}) => {

    const [prices, setPrices] = useState([]);

    const fetchPrices = useCallback(async () => {
        try {
          const response = await fetch(`http://127.0.0.1:5000//get_all_ticker/${ticker}`);
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          const data = await response.json();
          console.log('Fetched data:', data);
          setPrices(data);
          return data;
        } catch (error) {
          console.error('Error fetching data:', error);
          return []; // Return an empty array on error
        }
      }, []);

      /*
        {"label": "jan",
        "revenue": 64835,
        "cost": 12351}
       */
        // problem i see is that it is mapping everything, not solely the ticker that you want. So that means you need to make a url that gets all 
        // the data/objects with a certain ticker.

        // remove options if i dont need.

    useEffect(() => {
        fetchPrices();
    }, [fetchPrices]);

    return (
        <div className = "lineGraph">
            <Line
                data={{
                    labels: prices.map((price) => price.date),
                    datasets: [
                        {
                            label: ticker,
                            data: prices.map((price) => price.price),
                            backgroundColor: "#064FF0",
                            borderColor: "#064FF0"
                        }
                    ]
                }}
                options={{
                    responsive: true,
                    scales: {
                        x: {
                            type: 'category',
                            title: {
                                display: true,
                                text: 'Date'
                            }
                        },
                        y: {
                            type: 'linear',
                            title: {
                                display: true,
                                text: 'Price (In Dollars)'
                            }
                        }
                    }
                }}
                
            />
        </div>
    );
}

export default Graph;