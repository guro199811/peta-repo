
import { MapContainer, TileLayer } from "react-leaflet";

function ClinicsMap() {
    return (
        <div>
            <MapContainer>
                <TileLayer
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                />
                {/* Add your map markers here */}
            </MapContainer>
        </div>
    );
}

export default ClinicsMap;