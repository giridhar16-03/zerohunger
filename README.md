# FoodRescue AI - Vizag 🚀

**AI-Powered Hyper-Local Logistics for Food Rescue & Distribution**

An intelligent platform that uses **YOLOv8 computer vision** to verify food quality, connects restaurants/NGOs with volunteer drivers, and optimizes delivery routes using **OSRM** (Open Source Routing Machine).

---

## 📋 **Features**

✅ **AI Food Quality Detection** - YOLOv8 identifies food items and verifies quality  
✅ **User Authentication** - Login for Restaurants & Volunteer drivers  
✅ **Real-time Order Management** - Live database feed of all orders  
✅ **Smart Route Optimization** - OSRM calculates shortest routes  
✅ **Interactive Maps** - Leaflet.js for visualization  
✅ **OTP Verification** - Secure delivery confirmation  
✅ **Role-based Access** - Different dashboards for restaurants vs volunteers  

---

## 🛠️ **Tech Stack**

| Layer | Technology |
|-------|-----------|
| **Backend** | FastAPI (Python) |
| **Database** | SQLite (dev) / PostgreSQL (prod) |
| **AI/ML** | YOLOv8 (food detection) |
| **Frontend** | HTML5, CSS3, JavaScript |
| **Maps** | Leaflet.js, OpenStreetMap, OSRM |
| **Authentication** | LocalStorage + API validation |

---

## 📂 **Project Structure**

```
food_rescue/
├── backend/
│   ├── main.py              # FastAPI app & routes
│   ├── models.py            # SQLAlchemy ORM models
│   ├── database.py          # Database setup
│   ├── ai.py                # YOLOv8 food detection
│   ├── utils/               # Helper functions
│   ├── yolov8n.pt           # ML model (~6.5MB)
│   └── food_rescue.db       # SQLite database
│
├── frontend/
│   ├── index.html           # Main dashboard (redirects to login)
│   ├── login.html           # Authentication page
│   ├── restaurant.html      # Restaurant/NGO dashboard
│   ├── volunteer.html       # Driver/Volunteer dashboard
│   ├── script.js            # Frontend logic
│   └── style.css            # Styling
│
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── .gitignore             # Git ignore rules
```

---

## 🚀 **Quick Start (Local Development)**

### **Prerequisites**
- Python 3.8+
- Git
- Modern web browser

### **Step 1: Install Dependencies**
```bash
cd food_rescue
pip install -r requirements.txt
```

### **Step 2: Run Backend Server**
```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### **Step 3: Open in Browser**
```
http://localhost:8000
```

You'll be redirected to login page → Create account → Access dashboard

---

## 👤 **User Roles**

### **1. Restaurant/NGO Admin**
- Login URL: `http://localhost:8000/login.html` → Select "Restaurant"
- Upload food images for quality verification
- Monitor all orders
- Provide location for pickups

**Test Credentials:**
```
Username: restaurant1
Password: password123
```

### **2. Volunteer/Driver**
- Login URL: `http://localhost:8000/login.html` → Select "Volunteer"
- View available delivery requests
- Accept orders and navigate routes
- Verify delivery with OTP

**Test Credentials:**
```
Username: volunteer1
Password: password123
```

---

## 🔑 **API Endpoints**

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/register` | Create new account |
| POST | `/login` | User login |
| POST | `/analyze` | Analyze food image with AI |
| GET | `/orders` | Get all orders |
| POST | `/accept_order` | Accept pending order |
| POST | `/verify_otp` | Verify delivery |

---

## 📊 **Database Schema**

### **User Model**
```python
- id: Integer (PK)
- username: String
- hashed_password: String
- role: String (Restaurant/Volunteer)
- lat: Float
- lon: Float
- ngo_name: String (optional)
```

### **Order Model**
```python
- id: Integer (PK)
- food_item: String
- quantity: String
- pickup_time: String
- lat: Float
- lon: Float
- otp: String
- status: String (Pending/Accepted/Completed)
```

---

## 🌐 **Deployment Guide**

### **Option 1: Deploy Backend to Railway.app (Recommended)**

```bash
# Install railway CLI
npm install -g railway

# Login to railway
railway login

# Link project
railway init

# Deploy
railway up
```

Get your backend URL: `https://your-app.railway.app`

### **Option 2: Deploy to Render**

1. Connect GitHub repo to Render
2. Create new Web Service
3. Command: `cd backend && pip install -r ../requirements.txt && uvicorn main:app --host 0.0.0.0 --port $PORT`

### **Option 3: Deploy Frontend to GitHub Pages**

1. Copy `frontend/` files to `docs/` folder
2. Update API URL in `frontend/login.html` and `frontend/script.js`:
   ```javascript
   const API_URL = "https://your-backend-url.railway.app"
   ```
3. Push to GitHub
4. Enable GitHub Pages: Settings → Pages → Source: `docs/` folder

---

## 🔐 **Environment Variables (Production)**

Create `.env` file:
```
DATABASE_URL=postgresql://user:password@localhost/foodrescue
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=https://yourdomain.com
```

---

## 📝 **Development Notes**

- **Frontend checks authentication** before showing pages
- **Backend validates all requests** with user/role verification
- **YOLOv8 model** takes ~2GB storage (not in git, download locally)
- **SQLite** is used for local dev (replace with PostgreSQL for production)
- **OSRM is external API** (routes.openstreetmap.de) - always available

---

## 🐛 **Troubleshooting**

### **Backend not running?**
```bash
# Check if port 8000 is in use
lsof -i :8000

# Kill process
kill -9 <PID>

# Restart
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### **Frontend shows "Backend not running"?**
- Check backend is on `localhost:8000`
- Check browser console for CORS errors
- Verify API URL in `script.js`

### **Login redirects but no data loads?**
- Clear localStorage: `localStorage.clear()`
- Refresh page
- Check backend logs

---

## 📦 **Dependencies**

**Python (requirements.txt):**
- fastapi - Web framework
- uvicorn - ASGI server
- sqlalchemy - ORM
- ultralytics - YOLOv8
- pillow - Image processing
- python-multipart - File uploads

**Frontend (CDN):**
- Leaflet.js - Interactive maps
- OpenStreetMap - Map tiles
- OSRM API - Route planning

---

## 📄 **License**

MIT License - See LICENSE file

---

## 👨‍💻 **Contributors**

- Giridhar - Full Stack Developer

---

## 📞 **Support**

For issues or questions:
1. Check existing GitHub issues
2. Create new issue with detailed description
3. Include error logs and screenshots

---

## 🎯 **Roadmap**

- [ ] Mobile app (React Native)
- [ ] Real-time notifications (WebSockets)
- [ ] SMS alerts for drivers
- [ ] Payment integration
- [ ] Analytics dashboard
- [ ] Multi-language support

---

**Made with ❤️ for food rescue & sustainability**
