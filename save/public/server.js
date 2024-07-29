const express = require('express');
const path = require('path');

const app = express();
const port = 3000;

// Serve static files from the "public" directory
app.use(express.static(path.join(__dirname, '../templates')));

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '../templates','index.html'));
});

app.listen(port, () => {
    console.log(`Server running at http://127.0.0.1:${port}/`);
});