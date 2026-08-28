import streamlit as st
from PIL import Image
from database import init_db, save_scan, get_history
from model import load_model, classify_waste, WASTE_CLASSES
import components

st.set_page_config(
    page_title="EcoSort AI",
    page_icon="♻️",
    layout="wide"
)

init_db()

st.sidebar.title("🌱 EcoSort AI")
page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📷 Waste Scanner",
        "📊 Dashboard",
        "🚨 Smart Bins",
        "🏆 Green Score"
    ]
)
st.sidebar.divider()
st.sidebar.info("AI-powered waste identification and smart segregation assistant.")

if page == "🏠 Home":
    components.render_home()

elif page == "📷 Waste Scanner":
    st.title("📷 AI Waste Scanner")
    st.write("Upload an image of a waste item.")

    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Uploaded Waste", width=450)

        if st.button("🤖 Analyze Waste", use_container_width=True):
            with st.spinner("AI is analyzing the image..."):
                category, confidence = classify_waste(image)

            information = WASTE_CLASSES[category]
            st.divider()
            st.header("🤖 AI Result")

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Detected Category", category.upper())
                st.metric("AI Confidence", f"{confidence:.1f}%")
            with col2:
                st.metric("Recommended Bin", information["bin"])

            st.progress(min(confidence / 100, 1.0))
            st.info("💡 " + information["advice"])

            save_scan(
                waste=category,
                category=category,
                bin_name=information["bin"],
                confidence=confidence
            )
            st.success("✅ Scan saved successfully!")

elif page == "📊 Dashboard":
    st.title("📊 Eco Dashboard")
    data = get_history()

    if data.empty:
        st.warning("No scans yet. Go to Waste Scanner and analyze some images.")
    else:
        total = len(data)
        plastic = len(data[data["category"] == "plastic"])
        paper = len(data[data["category"] == "paper"])
        metal = len(data[data["category"] == "metal"])
        organic = len(data[data["category"] == "organic"])
        ewaste = len(data[data["category"] == "e-waste"])

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Scans", total)
        with col2:
            st.metric("♻️ Recyclable", plastic + paper + metal)
        with col3:
            st.metric("🌱 Organic", organic)
        with col4:
            st.metric("🔌 E-Waste", ewaste)

        st.divider()
        chart_data = data["category"].value_counts()
        st.subheader("Waste Category Distribution")
        st.bar_chart(chart_data)

        st.subheader("Recent Scans")
        st.dataframe(data, use_container_width=True)

elif page == "🚨 Smart Bins":
    components.render_smart_bins()

elif page == "🏆 Green Score":
    components.render_green_score()