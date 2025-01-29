const express = require('express');
const axios = require('axios');
const bodyParser = require('body-parser');
const cors = require('cors');
const path = require('path');
const winston = require('winston'); // Import Winston

const app = express();
app.use(cors());
app.use(bodyParser.json());

// Serve static files from the 'frontend' directory
app.use(express.static(path.join(__dirname, '../frontend')));

// Configure Winston
const logger = winston.createLogger({
    level: 'info',
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.json()
    ),
    transports: [
        new winston.transports.Console(), // Log to console
        new winston.transports.File({ filename: 'error.log', level: 'error' }), // Log errors to a file
        new winston.transports.File({ filename: 'combined.log' }) // Log all messages to a file
    ],
});

app.post('/api/chat', async (req, res) => {
    logger.info("Received message: " + req.body.message);  // Log incoming messages
    try {
        const userMessage = req.body.message;
        const response = await axios.post('http://localhost:8000/chat', { message: userMessage });
        
        logger.info("Response from Python backend: " + JSON.stringify(response.data));  // Log the response

        // Ensure that the response from the Python backend is properly structured
        res.json({ response: response.data.response });
    } catch (error) {
        logger.error("Error during processing request: " + error.message);  // Log errors
        res.status(500).json({ error: 'An error occurred while processing your request.' });
    }
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
    logger.info(`Server is running on port ${PORT}`);
});
