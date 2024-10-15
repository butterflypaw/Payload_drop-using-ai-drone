const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const http = require('http');
const socketIo = require('socket.io');
const missionRoutes = require('./routes/missionroutes');
const userRoutes = require('./routes/userroutes');
const { getTelemetryData, getDroneFeed } = require('./controllers/droneController');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);  // Set up WebSocket

// Middleware
app.use(cors());
app.use(express.json());

// Routes
app.use('/missions', missionRoutes);
app.use('/users', userRoutes);

// MongoDB connection
mongoose.connect('mongodb://localhost:27017/droneDB', { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => console.log('MongoDB connected'))
  .catch(err => console.log(err));

// WebSocket connections for telemetry and live feed
io.on('connection', (socket) => {
    console.log('New client connected');
    
    setInterval(() => {
        const telemetryData = getTelemetryData();  // Simulated telemetry data
        socket.emit('telemetry', telemetryData);
    }, 1000);  // Send telemetry data every 1 second

    setInterval(() => {
        const feedData = getDroneFeed();  // Simulated video feed data
        socket.emit('video-feed', feedData);
    }, 2000);  // Send live feed data every 2 seconds

    socket.on('disconnect', () => {
        console.log('Client disconnected');
    });
});

const PORT = process.env.PORT || 5000;
server.listen(PORT, () => console.log(`Server running on port ${PORT}`));
