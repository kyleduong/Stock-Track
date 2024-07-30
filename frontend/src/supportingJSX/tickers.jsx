export const fetchTickers = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/get_all_tickers_in_database/');
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const datas = await response.json();
      return datas;
    } catch (error) {
      console.error('Error fetching data:', error);
      return [];
    }
  };
//export const data =  fetch(`http://127.0.0.1:5000//get_all_tickers_in_database/`);

