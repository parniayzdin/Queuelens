import React from 'react'; // brings in core react libary
import ReactDOM from 'react-dom/client'; // This imports ReactDOM, which is responsible for actually drawing things on the page
import App from './App.jsx'; //This imports your main App componen, which defines what shows up in the browser
import './index.css';
import './leafletFix.js'; 
import 'leaflet/dist/leaflet.css'; 

ReactDOM.createRoot(document.getElementById('root')).render( //Find the root of my webpage in index.html, and render my entire React app inside it
  <React.StrictMode>
    <App />
  </React.StrictMode> //developer tool
);

