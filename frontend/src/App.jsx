import React, { useState, useEffect } from 'react';

import MainContent from './MainContent';
import PriceTable from './PriceTable';
import Modal from './Modal';
import './styles.css';

const App = () => {
  const [modalData, setModalData] = useState(null);
  const [imageUrl, setImageUrl] = useState('');

  useEffect(() => {
    fetch('/get_image_url')
      .then(response => response.json())
      .then(data => {
        setImageUrl(data.image_url);
      });
  }, []);

  const showImage = (item) => {
    fetch(`http://127.0.0.1:5000/get_ticker/${item}`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Item Not Found');
        }
        return response.json();
      })
      .then(data => {
        setModalData(data);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
        setModalData({ error: 'Item not found' });
      });
  };

  const scrapAlert = (itemName) => {
    // Implement the scraping logic here
    alert('Scraping Initiated for ' + itemName);
    console.log('Scraping:', itemName);
  };

  return (
      <div className="container">
        <div className="main-content">
          {/*<div className="left"> */}
            {/*<PriceHistory showImage={showImage} /> */}
          {/* </div>*/}
          {/*<div className="right">*/}
            <MainContent showImage={showImage} onScrap={scrapAlert}/>
          </div>
        {/*</div>*/}
        <PriceTable />
        {modalData && <Modal data={modalData} closeModal={() => setModalData(null)} />}
      </div>
  );
};

export default App;
