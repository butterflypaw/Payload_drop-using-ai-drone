const mongoose = require('mongoose');

const missionSchema = new mongoose.Schema({
    missionName: {
        type: String,
        required: true
    },
    waypoints: {
        type: Array,
        required: true
    }
});

module.exports = mongoose.model('Mission', missionSchema);
