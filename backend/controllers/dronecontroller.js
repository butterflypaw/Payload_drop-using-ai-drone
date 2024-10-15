const getTelemetryData = () => {
    return {
        altitude: (Math.random() * 100).toFixed(2),
        speed: (Math.random() * 50).toFixed(2),
        battery: (Math.random() * 100).toFixed(2)
    };
};

const getDroneFeed = () => {
    return `data:image/png;base64,${Buffer.from('sample image data').toString('base64')}`;
};

module.exports = { getTelemetryData, getDroneFeed };