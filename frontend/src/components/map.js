//AIzaSyBJyFrd8qkBZOaHD3MZuvGem1WJjGiCr5s
import React from 'react';
import { GoogleMap, LoadScript, Marker } from '@react-google-maps/api';

const mapContainerStyle = {
    height: "100%",
    width: "100%" 
};

const center = {
    lat: 17.374107667554952,
    lng:  78.52142885420501 
};

const MapComponent = () => {
    return (
        <LoadScript googleMapsApiKey="AIzaSyBJyFrd8qkBZOaHD3MZuvGem1WJjGiCr5s">
            <GoogleMap
                mapContainerStyle={mapContainerStyle}
                center={center}
                zoom={10}
            >
                <Marker position={center} />
            </GoogleMap>
        </LoadScript>
    );
};

export default MapComponent;
