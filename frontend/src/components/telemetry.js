import React, { useEffect, useState } from 'react';
import './Telemetry.css';

const Telemetry = () => {
    const [data, setData] = useState({
        altitude: '',
        speed: '',
        battery: '',
        gpsStatus: ''
    });

    useEffect(() => {
        const fetchTelemetryData = async () => {
            try {
                const response = await fetch('/api/telemetry');
                const telemetryData = await response.json();
                setData(telemetryData);
            } catch (error) {
                console.error('Error fetching telemetry data:', error);
            }
        };

        fetchTelemetryData();
        const intervalId = setInterval(fetchTelemetryData, 5000); 

        return () => clearInterval(intervalId); 
    }, []);

    return (
        <div className="telemetry">
            <h2 className="telemetry-heading">Altitude</h2>
            <p className="telemetry-value">{data.altitude} m</p>
            <h2 className="telemetry-heading">Speed</h2>
            <p className="telemetry-value">{data.speed} m/s</p>
            <h2 className="telemetry-heading">Battery</h2>
            <p className="telemetry-value">{data.battery}%</p>
            <h2 className="telemetry-heading">GPS Status</h2>
            <p className="telemetry-value">{data.gpsStatus}</p>
        </div>
    );
};

export default Telemetry;