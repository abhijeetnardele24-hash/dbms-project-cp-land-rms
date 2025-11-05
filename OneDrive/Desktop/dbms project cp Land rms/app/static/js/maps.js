// Property map visualization using Leaflet.js
let propertyMap = null;
let markers = [];

function initializeMap(mapId, lat, lng, zoom = 13) {
    if (propertyMap) {
        propertyMap.remove();
    }
    
    propertyMap = L.map(mapId).setView([lat || 19.0760, lng || 72.8777], zoom);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors',
        maxZoom: 19
    }).addTo(propertyMap);
    
    return propertyMap;
}

function addPropertyMarker(lat, lng, title, popupContent) {
    if (!propertyMap) return;
    
    const marker = L.marker([lat, lng]).addTo(propertyMap);
    if (title || popupContent) {
        marker.bindPopup(<b></b><br>);
    }
    markers.push(marker);
    return marker;
}

function addPropertyBoundary(coordinates, fillColor = '#3388ff') {
    if (!propertyMap || !coordinates) return;
    
    const polygon = L.polygon(coordinates, {
        color: fillColor,
        fillColor: fillColor,
        fillOpacity: 0.3
    }).addTo(propertyMap);
    
    propertyMap.fitBounds(polygon.getBounds());
    return polygon;
}

function clearMarkers() {
    markers.forEach(marker => marker.remove());
    markers = [];
}

// Calculate area of polygon
function calculateArea(coordinates) {
    if (!coordinates || coordinates.length < 3) return 0;
    
    let area = 0;
    for (let i = 0; i < coordinates.length; i++) {
        const j = (i + 1) % coordinates.length;
        area += coordinates[i][0] * coordinates[j][1];
        area -= coordinates[j][0] * coordinates[i][1];
    }
    return Math.abs(area / 2);
}
