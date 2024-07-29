import React from 'react';
import { Chart as ChartJS } from 'chart.js/auto';
import { Line } from 'react-chartjs-2';

import "index.html";
import "database.py";

export const App = () => {
    return (        
    <Line
      data={{
        labels: revenueData.map((data) => data.label),
        datasets: [
          {
            label: "Revenue",
            data: revenueData.map((data) => data.revenue),
            backgroundColor: "#064FF0",
            borderColor: "#064FF0",
          },
          {
            label: "Cost",
            data: revenueData.map((data) => data.cost),
            backgroundColor: "#FF3030",
            borderColor: "#FF3030",
          },
        ],
      }}
      options={{
        elements: {
          line: {
            tension: 0.5,
          },
        },
        plugins: {
          title: {
            text: "Monthly Revenue & Cost",
          },
        },
      }}
    />
  );
};

export default LineGraph;