const express = require('express');
const { createMission, getMissions } = require('../controllers/missioncontroller');
const router = express.Router();

router.post('/create', createMission);
router.get('/all', getMissions);

module.exports = router;
