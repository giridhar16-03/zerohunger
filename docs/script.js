
// --- CONFIGURATION ---
// UPDATE THIS WITH YOUR PRODUCTION BACKEND URL
const API_URL = window.location.hostname === 'localhost' 
    ? "http://localhost:8000" 
    : "https://YOUR-BACKEND-URL.railway.app";  // Change this to your production backend URL

const VIZAG_COORDS = [17.7100, 83.3000];  // Center of the map

let routeLine = null; // Global route line variable

// --- 1. INITIALIZE MAP (Leaflet.js) ---
const map = L.map('map').setView([17.71, 83.3], 13);

// Add the visual street tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Define Icons
const restaurantIcon = L.icon({
    iconUrl: 'https://cdn-icons-png.flaticon.com/512/3448/3448606.png', // Food Icon
    iconSize: [30, 30]
});
const shelterIcon = L.icon({
    iconUrl: 'https://cdn-icons-png.flaticon.com/512/25/25694.png', // Home Icon
    iconSize: [30, 30]
});

// Add Markers (Vizag Locations)
const pickup = L.marker([17.7100, 83.3000], {icon: restaurantIcon}).addTo(map).bindPopup("<b>Pickup:</b> Restaurant A").openPopup();
const dropoff = L.marker([17.7300, 83.3200], {icon: shelterIcon}).addTo(map).bindPopup("<b>Dropoff:</b> City Shelter");

// --- 2. DRAW ROUTE (OSRM API) ---
async function drawRoute() {
    const start = "83.3000,17.7100"; // OSRM uses Lon,Lat
    const end = "83.3200,17.7300";
    
    const url = `https://router.project-osrm.org/route/v1/driving/${start};${end}?overview=full&geometries=geojson`;
    
    try {
        const response = await fetch(url);
        const data = await response.json();
        const routeCoords = data.routes[0].geometry.coordinates.map(c => [c[1], c[0]]); // Flip to Lat,Lon for Leaflet
        
        // Draw the blue line
        L.polyline(routeCoords, {color: 'blue', weight: 5}).addTo(map);
        
        // Update Stats
        const distance = (data.routes[0].distance / 1000).toFixed(2); // Meters to KM
        document.getElementById('distValue').innerText = distance + " km";
    } catch(e) {
        console.log("Could not load route");
    }
}
drawRoute(); // Run immediately

// --- 3. ANALYZE FOOD (Talks to Python) ---
async function analyzeFood() {
    const input = document.getElementById('imageInput');
    const statusText = document.getElementById('statusText');
    const resultBox = document.getElementById('result');

    // 1. Validation
    if (input.files.length === 0) {
        alert("Please select an image first!");
        return;
    }

    // 2. Prepare Data
    const formData = new FormData();
    formData.append("file", input.files[0]);

    // 3. Update UI (Loading State)
    statusText.innerText = "🤖 AI Scanning...";
    statusText.style.color = "blue";
    resultBox.classList.remove('hidden');

    try {
        // 4. Send to Backend
        const response = await fetch(`${API_URL}/analyze`, {
            method: "POST",
            body: formData
        });

        // 5. Handle Response
        if (!response.ok) throw new Error("Backend Error");
        
        const data = await response.json();

        // 6. Update UI with AI Result
        document.getElementById('foodItem').innerText = data.item;
        document.getElementById('confScore').innerText = data.confidence;

        if (data.valid) {
            statusText.innerText = "✅ APPROVED";
            statusText.className = "success";
            fetchOrders(); // Refresh the database list
            alert("Food Verified! Driver Dispatching...");
        } else {
            statusText.innerText = "❌ REJECTED (Spoiled/Invalid)";
            statusText.className = "error";
        }

    } catch (error) {
        console.error(error);
        statusText.innerText = "⚠️ Error: Is Backend Running?";
        statusText.style.color = "orange";
    }
}

function getVolunteerLocation() {
    return new Promise((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(
            pos => resolve({
                lat: pos.coords.latitude,
                lon: pos.coords.longitude
            }),
            err => reject(err),
            { enableHighAccuracy: true }
        );
    });
}

async function getOSRMRoute(vLat, vLon, rLat, rLon) {
    const url = `https://router.project-osrm.org/route/v1/driving/${vLon},${vLat};${rLon},${rLat}?overview=full&geometries=geojson`;

    const res = await fetch(url);
    const data = await res.json();

    const route = data.routes[0];

    return {
        distance: (route.distance / 1000).toFixed(2), // km
        duration: (route.duration / 60).toFixed(1),   // minutes
        coordinates: route.geometry.coordinates
    };
}

function drawCustomRoute(coords) {
    if (routeLine) map.removeLayer(routeLine);

    const latLngs = coords.map(c => [c[1], c[0]]);
    routeLine = L.polyline(latLngs, {
        color: 'blue',
        weight: 5
    }).addTo(map);

    map.fitBounds(routeLine.getBounds());
}

// --- 4. FETCH HISTORY (Database) ---
async function fetchOrders() {
    try {
        const response = await fetch(`${API_URL}/orders`);
        const orders = await response.json();
        
        const list = document.getElementById('orderList');
        list.innerHTML = ""; // Clear existing list
        
        // Show newest first
        orders.slice().reverse().forEach(order => {
            const li = document.createElement('li');
            // Color code the status
            const color = order.status === "Approved" ? "green" : "red";
            li.innerHTML = `Order #${order.id}: <strong>${order.food_item}</strong> - <span style="color:${color}">${order.status}</span>`;
            list.appendChild(li);
        });
    } catch (e) {
        console.log("Database not connected yet");
    }
}

async function acceptOrder(orderId) {
    const res = await fetch(API_URL + "/accept_order", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ order_id: orderId })
    });

    const data = await res.json();

    if (data.status === "success") {
        showRouteToRestaurant(data.dest_lat, data.dest_lon);
    }
}

// 🔐 Logout Function
function logout() {
    localStorage.removeItem("user");
    localStorage.removeItem("role");
    localStorage.removeItem("myLat");
    localStorage.removeItem("myLon");
    window.location.href = "login.html";
}

// Load database orders when page opens
fetchOrders();
