import streamlit as st
from PIL import Image
import torch
from transformers import CLIPModel, CLIPProcessor

WASTE_CLASSES = {
    "plastic": {
        "bin": "🔵 Dry / Recyclable Waste",
        "advice": "Clean and empty the plastic item before placing it in recyclable waste.",
        "score": 10
    },
    "paper": {
        "bin": "🔵 Dry / Recyclable Waste",
        "advice": "Keep paper dry and separate it from food-contaminated waste.",
        "score": 10
    },
    "metal": {
        "bin": "🔵 Dry / Recyclable Waste",
        "advice": "Separate metal items from wet waste and send them for recycling.",
        "score": 10
    },
    "glass": {
        "bin": "🔵 Dry / Recyclable Waste",
        "advice": "Handle glass carefully and place it in the appropriate collection container.",
        "score": 10
    },
    "organic": {
        "bin": "🟢 Wet / Organic Waste",
        "advice": "Put food and biodegradable material into the organic-waste stream.",
        "score": 10
    },
    "e-waste": {
        "bin": "🟣 E-Waste Collection",
        "advice": "Do not mix electronic items with normal household waste. Use an authorized e-waste collection system.",
        "score": 15
    }
}

@st.cache_resource
def load_model():
    model_name = "openai/clip-vit-base-patch32"
    model = CLIPModel.from_pretrained(model_name)
    processor = CLIPProcessor.from_pretrained(model_name)
    return model, processor

def classify_waste(image):
    model, processor = load_model()

    labels = [
        "a plastic bottle or plastic item",
        "paper or cardboard",
        "a metal can or metal object",
        "a glass bottle or glass object",
        "food waste or organic waste",
        "an electronic device or electronic waste"
    ]

    categories = ["plastic", "paper", "metal", "glass", "organic", "e-waste"]

    inputs = processor(
        text=labels,
        images=image,
        return_tensors="pt",
        padding=True
    )

    with torch.no_grad():
        outputs = model(**inputs)

    probabilities = outputs.logits_per_image.softmax(dim=1)[0]
    best_index = probabilities.argmax().item()

    category = categories[best_index]
    confidence = probabilities[best_index].item() * 100

    return category, confidence