const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');

const app = express();

// // Enable CORS with specific options
// const corsOptions = {
//     origin: "http://localhost:3000",
//     methods: ["GET", "POST", "DELETE", "PUT"],
//     allowedHeaders: ["Content-Type", "Authorization", "Anil"],
// };

// // Use CORS and body-parser middleware
// app.use(cors(corsOptions));
// app.use(bodyParser.json());

// Custom headers can be added here if needed
app.use((req, res, next) => {
    res.header("Access-Control-Allow-Methods", "DELETE, GET, POST, PUT");
    res.header("Access-Control-Allow-Origin", "");
    res.header("Access-Control-Allow-Headers", "Content-Type, Authorization, Anil");
    next();
});

// Home route
app.get('/', (req, res) => {
    res.send('Hello, World! from server 2 by node');
});

// API data route
app.route('/api/data')
    .get((req, res) => {
        const data = { message: "Hello, this is your data!", status: "success" };
        res.json(data);
    })
    .post((req, res) => {
        const incomingData = req.body;
        const message = incomingData.message || 'No message received';

        const responseData = {
            message: `Received: ${message}`,
            status: "success"
        };
        res.json(responseData);
    })
    .put((req, res) => {
        const incomingData = req.body;
        const message = incomingData.message || 'No message received';

        const responseData = {
            message: `Updated: ${message}`,
            status: "success"
        };
        res.json(responseData);
    });

// Delete route
app.delete('/api/delete', (req, res) => {
    const responseData = {
        message: "Data deleted successfully",
        status: "success"
    };
    res.json(responseData);
});

// Start the server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
