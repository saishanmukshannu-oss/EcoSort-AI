import streamlit as st
from database import get_history

def render_home():
    st.title("🌱 EcoSort AI")
    st.subheader("AI-Powered Smart Waste Segregation System")
    st.write("EcoSort AI helps people identify waste, choose the appropriate disposal category, and make better segregation decisions.")
    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("♻️ Smart Classification", "AI")
    with col2:
        st.metric("🌍 Environmental Goal", "Cleaner Waste")
    with col3:
        st.metric("🏆 Green Engagement", "Scoring")

    st.divider()
    st.header("How it works")
    st.markdown("""
    ### 1️⃣ Upload
    Upload a photograph of a waste item.
    ### 2️⃣ AI Analysis
    The computer-vision model analyzes the image.
    ### 3️⃣ Classification
    The system predicts the most likely waste category.
    ### 4️⃣ Disposal Guidance
    EcoSort AI recommends the appropriate waste stream.
    ### 5️⃣ Data & Dashboard
    Scan results are stored and displayed through statistics.
    ### 6️⃣ Smart Bin Monitoring
    Bin-fill information can be connected to the dashboard.
    """)
    st.success("♻️ Better segregation → Better recycling → Cleaner environment")

def render_smart_bins():
    st.title("🚨 Smart Bin Monitoring")
    st.write("This dashboard demonstrates how sensor-based bin monitoring can be integrated with EcoSort AI.")
    st.divider()

    bin1, bin2, bin3 = 35, 72, 94
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("🟢 Bin A")
        st.metric("Fill Level", f"{bin1}%")
        st.progress(bin1 / 100)
        st.success("Normal")

    with col2:
        st.subheader("🟡 Bin B")
        st.metric("Fill Level", f"{bin2}%")
        st.progress(bin2 / 100)
        st.warning("Getting Full")

    with col3:
        st.subheader("🔴 Bin C")
        st.metric("Fill Level", f"{bin3}%")
        st.progress(bin3 / 100)
        st.error("Collection Required")

    st.divider()
    st.subheader("Future IoT Integration")
    st.markdown("**Ultrasonic Sensor** → **ESP32** → **Internet / Wi-Fi** → **EcoSort Dashboard** → **Collection Alert**")

def render_green_score():
    st.title("🏆 Green Score")
    data = get_history()
    total_scans = len(data)
    score = 0 if total_scans == 0 else total_scans * 10

    st.metric("🌱 Your Green Score", score)
    st.progress(min(score / 500, 1.0))

    if score < 100:
        level = "🌱 Eco Starter"
    elif score < 250:
        level = "♻️ Eco Helper"
    elif score < 500:
        level = "🌍 Eco Warrior"
    else:
        level = "🏆 Green Champion"

    st.subheader(f"Current Level: {level}")
    st.divider()
    st.subheader("How points are earned")
    st.write("♻️ Waste correctly classified → +10 points")
    st.write("🌱 Organic waste identification → +10 points")
    st.write("🔌 E-waste identification → +15 points")
    st.write("🏆 More scans → Higher Green Score")
    st.divider()
    st.success("Every correct segregation decision contributes towards a cleaner environment! 🌍")