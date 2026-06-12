import streamlit as st
from ultralytics import YOLO
from PIL import Image
import numpy as np
import pandas as pd
import time

# --- CONFIGURATION ---
st.set_page_config(page_title="Zero_Hunger", page_icon="🍔")

# --- 1. THE EYE (AI LOGIC) ---
# @st.cache_resource keeps the model in memory so it doesn't reload every time
@st.cache_resource
def load_model():
    return YOLO('yolov8n.pt') # Downloads automatically the first time

model = load_model()

# List of valid foods (Standard COCO classes)
VALID_FOODS = ['banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake']

def analyze_image(image):
    """Runs AI detection on the uploaded image"""
    results = model(image)
    detected_items = []
    is_food = False
    
    # Check results
    for result in results:
        for box in result.boxes:
            class_name = model.names[int(box.cls[0])]
            conf = float(box.conf[0])
            
            if class_name in VALID_FOODS and conf > 0.4:
                detected_items.append(f"{class_name} ({int(conf*100)}%)")
                is_food = True
    
    # Return the image with boxes drawn (plot() returns a numpy array)
    annotated_img = results[0].plot() 
    return is_food, detected_items, annotated_img

# --- 2. THE FACE (FRONTEND) ---
st.title("Hyper-Local Food Rescue")
st.markdown("### Match Excess Food with Drivers Instantly")

# Sidebar for "User Role" simulation
role = st.sidebar.radio("Select Role", ["Donor (Restaurant)", "Driver (Volunteer)"])

if role == "Donor (Restaurant)":
    st.header("Step 1: Quality Control")
    st.write("Take a photo of the food to verify quality and safety.")
    
    uploaded_file = st.file_uploader("Upload Food Photo", type=['jpg', 'png', 'jpeg'])
    
    if uploaded_file:
        # Convert file to Image for AI
        image = Image.open(uploaded_file)
        
        # Display loading state
        with st.spinner('AI is analyzing food quality...'):
            time.sleep(1.5) # Fake delay for dramatic effect
            is_valid, items, result_img = analyze_image(image)
        
        # Show Results
        col1, col2 = st.columns(2)
        with col1:
            st.image(image, caption="Original", use_container_width=True)
        with col2:
            st.image(result_img, caption="AI Analysis", use_container_width=True, channels="BGR") # BGR to RGB fix might be needed depending on system, usually Streamlit handles it.
            st.image(result_img, caption="AI Analysis", use_container_width=True, channels="BGR") # BGR to RGB fix might be needed depending on system, usually Streamlit handles it.
            
        if is_valid:
            st.success(f"**Approved!** Detected: {', '.join(items)}")
            if st.button("Broadcast to Drivers"):
                st.toast("Broadcasting request to 5 nearby drivers...", icon="🔔")
                time.sleep(2)
                st.success("Drivers notified! Order #4928 created.")
        else:
            st.error("**Rejected.** No recognizable food detected.")
            st.warning("System detects: " + (", ".join(items) if items else "Nothing recognized"))

elif role == "Driver (Volunteer)":
    st.header("Step 2: Driver Dashboard")
    
    # Mock Data for the Map
    # Coordinates for a simple city route (Example: New York/Generic)
    map_data = pd.DataFrame({
        'lat': [40.7128, 40.7150, 40.7180],
        'lon': [-74.0060, -74.0020, -74.0080],
        'type': ['Driver', 'Pickup', 'Shelter']
    })
    
    st.info("**New Alert:** Pickup at 'Joe's Pizza' (1.2 km away)")
    
    # Simple Map
    st.map(map_data)
    
    with st.expander("View Trip Details", expanded=True):
        st.markdown("""
        * **Pickup:** Joe's Pizza (Expires in 45 mins)
        * **Drop-off:** City Shelter #4
        * **Total Distance:** 2.4 km
        """)
        
    if st.button("Accept Job"):
        st.balloons()
        st.success("Job Accepted! Navigation started.")