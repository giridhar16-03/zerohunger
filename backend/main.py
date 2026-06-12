from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

import models, database
import random

# -------------------- DATABASE INIT --------------------
database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

def health():
    return {"status": "ok"}

# -------------------- CORS --------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"],
    allow_credentials=True,
)

# -------------------- DB DEPENDENCY --------------------
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==================== AUTH ROUTES ====================

@app.post("/register")
async def register(data: dict, db: Session = Depends(get_db)):
    username = data.get("username")

    if not username:
        raise HTTPException(status_code=400, detail="Username required")

    # ✅ CHECK FOR EXISTING USER (CRITICAL FIX)
    existing_user = db.query(models.User).filter(
        models.User.username == username
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    print(f"Registering {username} at {data.get('lat')}, {data.get('lon')}")

    new_user = models.User(
        username=username,
        hashed_password=data.get("password"),
        role=data.get("role"),
        lat=float(data.get("lat")),
        lon=float(data.get("lon")),
        ngo_name=data.get("ngo_name", "")
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"status": "success", "message": "User registered"}

@app.post("/login")
async def login(data: dict, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.username == data.get("username"),
        models.User.hashed_password == data.get("password")
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    return {
        "status": "success",
        "role": user.role,
        "lat": user.lat,
        "lon": user.lon
    }

# ==================== ORDER ROUTES ====================

from ai import analyze_image
from PIL import Image
import io

@app.post("/analyze")
async def analyze(
    file: UploadFile = File(...),
    lat: float = Form(default=17.7100),
    lon: float = Form(default=83.3000),
    quantity: str = Form(default="1 unit"),
    time: str = Form(default="ASAP"),
    db: Session = Depends(get_db)
):
    # Read image
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    is_valid, items = analyze_image(image)

    if not is_valid:
        raise HTTPException(
            status_code=400,
            detail="Rejected: Food quality not verified"
        )

    # Create order ONLY if AI approves
    otp = str(random.randint(1000, 9999))
    new_order = models.Order(
        food_item=", ".join(items),
        quantity=quantity,
        pickup_time=time,
        lat=lat,
        lon=lon,
        otp=otp,
        status="Pending"
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return {
        "status": "success",
        "item": "AI Verified Food",
        "detected": items,
        "order_id": new_order.id
    }


@app.get("/orders")
async def get_all_orders(db: Session = Depends(get_db)):
    return db.query(models.Order).all()

@app.post("/accept_order")
async def accept_order(data: dict, db: Session = Depends(get_db)):
    order_id = data.get("order_id")

    order = db.query(models.Order).filter(
        models.Order.id == order_id
    ).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status != "Pending":
        raise HTTPException(status_code=400, detail="Order already taken")

    order.status = "Accepted"
    db.commit()

    return {
        "status": "success",
        "otp": order.otp,
        "dest_lat": order.lat,
        "dest_lon": order.lon
    }

@app.post("/verify_otp")
async def verify_otp(data: dict, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(
        models.Order.id == data.get("order_id")
    ).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.otp != data.get("otp_code"):
        raise HTTPException(status_code=400, detail="Wrong OTP")

    order.status = "Completed"
    db.commit()

    return {"status": "success", "message": "Delivery completed"}

# -------------------- STATIC FILES --------------------
import os
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="static")
