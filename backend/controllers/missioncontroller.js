const Mission = require('../models/mission');

const createMission = async (req, res) => {
    const { missionName, waypoints } = req.body;
    try {
        const mission = new Mission({ missionName, waypoints });
        await mission.save();
        res.status(201).json({ message: 'Mission created successfully' });
    } catch (error) {
        res.status(500).json({ message: 'Error creating mission', error });
    }
};

const getMissions = async (req, res) => {
    try {
        const missions = await Mission.find();
        res.status(200).json(missions);
    } catch (error) {
        res.status(500).json({ message: 'Error retrieving missions', error });
    }
};

module.exports = { createMission, getMissions };
