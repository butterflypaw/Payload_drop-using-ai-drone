import React, { useRef, useState } from 'react';
import Navbar from './components/Navbar';
import MissionPlanner from './components/missionplanner';
import Telemetry from './components/telemetry';
import GoogleEarth from './components/map';
import './App.css';

function App() {
    const [telemetryWidth, setTelemetryWidth] = useState(250);
    const resizerRef = useRef(null);

    const handleMouseDown = (e) => {
        e.preventDefault();
        const startWidth = telemetryWidth;

        const mouseMoveHandler = (event) => {
            const newWidth = startWidth + (event.clientX - e.clientX);
            setTelemetryWidth(newWidth > 200 ? newWidth : 200);
        };

        const mouseUpHandler = () => {
            document.removeEventListener('mousemove', mouseMoveHandler);
            document.removeEventListener('mouseup', mouseUpHandler);
        };

        document.addEventListener('mousemove', mouseMoveHandler);
        document.addEventListener('mouseup', mouseUpHandler);
    };

    return (
        <div className="app-container">
            <div className="navbar-container">
                <Navbar /> 
            </div>
            <div className="map-telemetry-container">
                <div 
                    className="telemetry-container" 
                    style={{ width: `${telemetryWidth}px` }}
                >
                    <Telemetry />
                </div>
                <div 
                    className="resizer" 
                    ref={resizerRef} 
                    onMouseDown={handleMouseDown} 
                />
                <div className="map-container">
                    <GoogleEarth /> 
                </div>
            </div>
            <div className="mission-planner-container">
                <MissionPlanner />
            </div>
        </div>
    );
}

export default App;