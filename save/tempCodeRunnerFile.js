// Serve static files from the "public" directory
app.use(express.static(path.join(__dirname, 'public')));