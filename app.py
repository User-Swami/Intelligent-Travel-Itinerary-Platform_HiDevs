import streamlit as st
from langchain_groq import ChatGroq

# Set page config with theme
st.set_page_config(page_title="🌍 Travel Itinerary Generator", layout="wide")

# Custom CSS for dark brown background and black text
st.markdown("""
    <style>
        body {
            background-color: #DDA0DD; /* Dark Brown */
            color: #8B008B; /* Black text */
        }
        .stApp {
            background-color: #DDA0DD; /* Dark Brown */
            color: #8B008B; /* Black text */
            padding: 2rem;
        }
        .big-title {
            font-size: 48px;
            font-weight: bold;
            color: #8B008B; /* Black title text */
        }
        .info-box {
            background: #d7ccc8; /* Lighter brown shade for contrast */
            color: #8B008B;
            padding: 1rem;
            border-radius: 10px;
            margin-top: 1rem;
        }
        .sidebar .css-1d391kg {
            background-color: #5d4037; /* Darker sidebar brown */
            color: #8B008B;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<div class='big-title'>🌍 Intelligent Travel Itinerary Generator 🌍</div>", unsafe_allow_html=True)
st.markdown("Get personalized travel plans powered by AI!")

# Sidebar input
with st.sidebar:
    st.header("🛫 Trip Preferences")
    explorer = st.text_input("Traveler / Explorer", "Adventurer")
    days = st.slider("Trip Duration (Days)", 1, 15, 5)
    places = [
        "Paris, France", "Tokyo, Japan", "New York, USA", "Rome, Italy", "Barcelona, Spain",
        "Dubai, UAE", "London, UK", "Bangkok, Thailand", "Istanbul, Turkey", "Sydney, Australia"
    ]
    destination = st.selectbox("Select Destination", places)
    interests = st.multiselect(
        "Interests",
        ["Culture", "Food", "Nature", "Adventure", "Shopping", "Relaxation", "History"],
        default=["Culture", "Food"]
    )
    generate = st.button("✨ Generate Itinerary")

# Itinerary generation
if generate:
    with st.spinner("🧳 Planning your epic journey..."):
        llm = ChatGroq(
            model="llama3-8b-8192",
            api_key="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")

        prompt = f"""
Create a {days}-day travel itinerary for an explorer named {explorer}, visiting {destination}.
They enjoy: {', '.join(interests)}.
Include must-visit places, unique food spots, cultural experiences, and organize it day-by-day.
""" 
        try:
            result = llm.invoke(prompt)
            st.success("✅ Your Itinerary is Ready!")
            st.markdown(f"<div class='info-box'><strong>🗓️ {days}-Day Plan for {destination}</strong><br><br>{result.content}</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error("Something went wrong while generating the itinerary.")
            st.exception(e)

# Footer
st.markdown("---")
st.markdown("🚀 Powered by Streamlit & Groq")
