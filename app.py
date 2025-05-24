import streamlit as st
from langchain_groq import ChatGroq

# ---------- Dummy Destination Data ----------
DUMMY_PLACES = [
    {
        "city": "Paris",
        "country": "France",
        "attractions": ["Eiffel Tower", "Louvre Museum", "Notre-Dame Cathedral"],
        "food": ["Croissants", "Macarons", "French Onion Soup"],
        "culture": ["Art", "Fashion", "History"]
    },
    {
        "city": "Delhi",
        "country": "India",
        "attractions": ["Red Fort", "Qutub Minar", "India Gate"],
        "food": ["Chole Bhature", "Paratha", "Butter Chicken"],
        "culture": ["Heritage", "Festivals", "Mughal Architecture"]
},
{
        "city": "Mumbai",
        "country": "India",
        "attractions": ["Gateway of India", "Marine Drive", "Elephanta Caves"],
        "food": ["Vada Pav", "Pav Bhaji", "Bombay Sandwich"],
        "culture": ["Bollywood", "Street Life", "Diverse Communities"]
    },
    {
        "city": "Jaipur",
        "country": "India",
        "attractions": ["Hawa Mahal", "Amber Fort", "City Palace"],
        "food": ["Dal Baati Churma", "Ghewar", "Laal Maas"],
        "culture": ["Royalty", "Handicrafts", "Rajasthani Folk Music"]
    },
    {
        "city": "Kolkata",
        "country": "India",
        "attractions": ["Victoria Memorial", "Howrah Bridge", "Dakshineswar Temple"],
        "food": ["Rosogolla", "Macher Jhol", "Kathi Roll"],
        "culture": ["Literature", "Art", "Colonial Architecture"]
    },
    {
        "city": "Kerala",
        "country": "India",
        "attractions": ["Alleppey Backwaters", "Munnar Hills", "Padmanabhaswamy Temple"],
        "food": ["Appam with Stew", "Puttu and Kadala Curry", "Banana Chips"],
        "culture": ["Ayurveda", "Classical Dance (Kathakali)", "Festivals like Onam"]
    },
        {
        "city": "Tokyo",
        "country": "Japan",
        "attractions": ["Tokyo Tower", "Shibuya Crossing", "Senso-ji Temple"],
        "food": ["Sushi", "Ramen", "Tempura"],
        "culture": ["Technology", "Anime", "Tradition"]
    },
    {
        "city": "New York City",
        "country": "USA",
        "attractions": ["Statue of Liberty", "Times Square", "Central Park"],
        "food": ["Cheesecake", "Hot Dogs", "Bagels"],
        "culture": ["Diversity", "Theater (Broadway)", "Fashion"]
    },
    {
        "city": "Rome",
        "country": "Italy",
        "attractions": ["Colosseum", "Trevi Fountain", "Vatican City"],
        "food": ["Pasta", "Gelato", "Pizza"],
        "culture": ["History", "Art", "Architecture"]
    },
    {
        "city": "Istanbul",
        "country": "Turkey",
        "attractions": ["Hagia Sophia", "Blue Mosque", "Grand Bazaar"],
        "food": ["Kebabs", "Baklava", "Turkish Tea"],
        "culture": ["Ottoman Heritage", "Spices", "East-Meets-West"]
    },
    {
        "city": "Bangkok",
        "country": "Thailand",
        "attractions": ["Grand Palace", "Wat Arun", "Chatuchak Market"],
        "food": ["Pad Thai", "Green Curry", "Mango Sticky Rice"],
        "culture": ["Buddhism", "Street Markets", "Festivals like Songkran"]
    }
]

# ---------- Utility Functions ----------
def get_place_info(destination_name):
    for place in DUMMY_PLACES:
        if destination_name.split(",")[0].strip().lower() in place["city"].lower():
            return place
    return None

def get_similar_places(destination, interests):
    matched = []
    place_info = get_place_info(destination)
    if not place_info:
        return matched
    for category in ["attractions", "food", "culture"]:
        for interest in interests:
            if interest.lower() in [item.lower() for item in place_info.get(category, [])]:
                matched.extend(place_info.get(category, []))
    return list(set(matched))[:5]  # top 5 matches

def generate_itinerary(explorer, destination, interests, days, place_info=None):
    prompt = f"""
You are a travel planner AI. Create a {days}-day travel itinerary for {explorer}, who is visiting {destination}.
They are interested in: {', '.join(interests)}.
Incorporate the following destination data in your suggestions if available: {place_info}.
Ensure the itinerary includes must-see places, local foods, cultural spots, and is organized by day.
"""
    llm = ChatGroq(model="llama3-8b-8192", api_key="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")
    return llm.invoke(prompt).content

# ---------- Streamlit UI ----------
st.set_page_config(page_title="🌍 Travel Itinerary Generator", layout="wide")

st.markdown("""
    <style>
        body {
            background-color: #DDA0DD;
            color: #8B008B;
        }
        .stApp {
            background-color: #DDA0DD;
            color: #8B008B;
            padding: 2rem;
        }
        .big-title {
            font-size: 48px;
            font-weight: bold;
            color: #8B008B;
        }
        .info-box {
            background: #d7ccc8;
            color: #8B008B;
            padding: 1rem;
            border-radius: 10px;
            margin-top: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='big-title'>🌍 Intelligent Travel Itinerary Generator 🌍</div>", unsafe_allow_html=True)
st.markdown("Get personalized travel plans powered by AI!")

with st.sidebar:
    st.header("🛫 Trip Preferences")
    explorer = st.text_input("Traveler / Explorer", "Adventurer")
    days = st.slider("Trip Duration (Days)", 1, 15, 5)
    places = [f"{place['city']}, {place['country']}" for place in DUMMY_PLACES]
    destination = st.selectbox("Select Destination", places)
    interests = st.multiselect(
        "Interests",
        ["Art", "History", "Food", "Fashion", "Nature", "Technology", "Adventure", "Tradition"],
        default=["Art", "Food"]
    )
    generate = st.button("✨ Generate Itinerary")

if generate:
    with st.spinner("🧳 Planning your epic journey..."):
        try:
            place_info = get_place_info(destination)
            recommendations = get_similar_places(destination, interests)
            result = generate_itinerary(explorer, destination, interests, days, place_info)

            st.success("✅ Your Itinerary is Ready!")
            st.markdown(f"<div class='info-box'><strong>🗓️ {days}-Day Plan for {destination}</strong><br><br>{result}</div>", unsafe_allow_html=True)

            if recommendations:
                st.markdown("### 🔍 Recommended Places Based on Your Interests:")
                for rec in recommendations:
                    st.markdown(f"- {rec}")
        except Exception as e:
            st.error("❌ Something went wrong while generating the itinerary.")
            st.exception(e)

st.markdown("---")
st.markdown("🚀 Powered by Streamlit & Groq")
