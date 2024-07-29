import React from 'react';
import Graph from "./supportingJSX/graph.jsx"

const Modal = ({ data, closeModal }) => (
  <div className="modal" style={{ display: 'flex' }}>
    <div className="modal-content">
      <span className="close" onClick={closeModal}>&times;</span>
      <div className="modal-header">
        <h2 id="modal-ticker">{data.error ? 'Error' : `Ticker: ${data.ticker}`}</h2>
      </div>
      <div className="modal-header">
        <h2 id="modal-price">{data.error ? data.error : `Price: ${data.price}`}</h2>
      </div>
      <div className="modal-body">
        <p id="modal-date">Last Scrape Date: {data.date}</p>
        <div id="modal-graph">
          {/* Graph can be rendered here */}
          <Graph ticker={`${data.ticker}`}/>
          <canvas id="graph-canvas"></canvas>
        </div>
      </div>
    </div>
  </div>
);

export default Modal;
