import { useState, useEffect } from 'react'; 
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import './index.css';
import axios from "axios";
import icon2x from 'leaflet/dist/images/marker-icon-2x.png';
import icon from 'leaflet/dist/images/marker-icon.png';
import shadow from 'leaflet/dist/images/marker-shadow.png';

delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: icon2x,
  iconUrl: icon,
  shadowUrl: shadow,
});

function ChangeView({ center }) {
  const map = useMap();
  useEffect(() => {
    if (center) map.setView(center);   // or map.flyTo(center, 13);
  }, [center, map]);
  return null;
}

export default function App() {
  const [reports, setReports] = useState([]);
  const [now, setNow] = useState(Date.now());
  const [query, setQuery] = useState("");           
  const [searchResult, setSearchResult] = useState(null);  
  const [center, setCenter] = useState([43.65, -79.38]);
  const [waitMinutes, setWaitMinutes] = useState('');
  const [ttlMinutes, setTtlMinutes] = useState(60); 

  const fetchReports = () => {
    fetch('http://127.0.0.1:8000/reports/')
      .then(r => r.json())
      .then(setReports)
      .catch(console.error);
  };

  const handleReport = async () => {
    if (!searchResult) {
      alert("Search for a place first.");
      return;
    }
    if (!waitMinutes) {
      alert("Enter wait time in minutes.");
      return;
    }

    try {
      await axios.post("http://127.0.0.1:8000/reports/", {
        Name: searchResult.query,
        lat: searchResult.lat,
        lon: searchResult.lon,
        wait_minutes: Number(waitMinutes),
        ttl_minutes: Number(ttlMinutes),
      });
      setWaitMinutes('');
      fetchReports(); 
    } catch (err) {
      console.error("POST failed:", err.response?.data || err.message);
      alert("Could not save the report.");
    }
  };

  const handleSearch = async () => {
    if (!query) return;
    try {
      const res = await axios.get(`http://127.0.0.1:8000/reports/search`, {
        params: { query },
      });
      setSearchResult(res.data);
      setCenter([res.data.lat, res.data.lon]);
    } catch (err) {
      console.error("Search failed", err);
      alert("Could not find that location.");
    }
  };

  useEffect(() => {
    fetchReports();
    const pid = setInterval(fetchReports, 15000);
    return () => clearInterval(pid);
  }, []);

  useEffect(() => {
    const tid = setInterval(() => setNow(Date.now()), 30000);
    return () => clearInterval(tid);
  }, []);

  const minutesLeft = (r) => {
    const expires = new Date(r.created_at).getTime() + r.ttl_minutes * 60000;
    const diff = expires - now;
    return diff > 0 ? Math.ceil(diff / 60000) : 0;
  };

  return (
    <>
      <div style={{ padding: "10px", display: "flex", gap: "10px", background: "#fff", zIndex: 1000 }}>
        <input
          type="text"
          placeholder="Search a location..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          style={{ padding: "8px", width: "300px" }} />
        <button onClick={handleSearch} style={{ padding: "8px" }}>
          Search
        </button>
        <input
          type="number"
          placeholder="Wait (min)"
          value={waitMinutes}
          onChange={(e) => setWaitMinutes(e.target.value)}
          style={{ width: 100, padding: 8 }}
        />
        <button onClick={handleReport} style={{ padding: "8px" }}>
          Report wait
        </button>
      </div>

      <MapContainer
        center={center}
        zoom={13}
        style={{
          height: searchResult ? 'calc(100vh - 120px)' : 'calc(100vh - 60px)',
          width: '100vw'
        }}
      >
        <ChangeView center={center} />
        <TileLayer
          attribution="&copy; OpenStreetMap contributors"
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

        {reports.map(r => (
          <Marker key={r.id} position={[r.lat, r.lon]}>
            <Popup>
              Original wait: <b>{r.wait_minutes} min</b><br />
              Expires in: <b>{minutesLeft(r)} min</b>
            </Popup>
          </Marker>
        ))}

        {searchResult && (
          <Marker position={[searchResult.lat, searchResult.lon]}>
            <Popup>{searchResult.query}</Popup>
          </Marker>
        )}
      </MapContainer>
    </>
  );
}