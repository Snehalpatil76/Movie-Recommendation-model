import streamlit as st
import pandas as pd
from PIL import Image
import random

# Placeholder data
def load_placeholder_movies():
    return [
        {"title": "The Matrix", "banner": "https://via.placeholder.com/300x450.png?text=The+Matrix"},
        {"title": "Inception", "banner": "https://via.placeholder.com/300x450.png?text=Inception"},
        {"title": "Interstellar", "banner": "https://via.placeholder.com/300x450.png?text=Interstellar"},
        {"title": "The Dark Knight", "banner": "https://via.placeholder.com/300x450.png?text=The+Dark+Knight"},
        {"title": "Avengers", "banner": "https://via.placeholder.com/300x450.png?text=Avengers"},
        {"title": "Titanic", "banner": "https://via.placeholder.com/300x450.png?text=Titanic"},
    ]

# Mock function to simulate movie recommendations
def get_recommendations(movie_name):
    # In actual code, replace with your ML model logic
    random.shuffle(placeholder_movies)
    return placeholder_movies[:5]

# UI Styling
st.set_page_config(page_title="MovieRecs", layout="wide")
st.markdown("""
    <style>
        body {
            background-color: #0D1B2A;
        }
        .block-container {
            padding-top: 2rem;
        }
        .movie-banner {
            border-radius: 12px;
            transition: transform 0.2s;
        }
        .movie-banner:hover {
            transform: scale(1.05);
        }
        h2, h3, label, p {
            color: #ffffff;
        }
    </style>
""", unsafe_allow_html=True)

placeholder_movies = load_placeholder_movies()

st.title("🍿 Movie Recommendations")

movie_name = st.text_input("Search for a movie:", "")

if movie_name:
    recommended = get_recommendations(movie_name)
    st.subheader("🎯 Recommended for You")
else:
    st.subheader("🔥 Trending Now")
    recommended = placeholder_movies

cols = st.columns(5)
for idx, movie in enumerate(recommended):
    with cols[idx % 5]:
        st.image(movie["banner"], caption=movie["title"], use_column_width=True)

# Additional carousels (Trending, Top Rated, Recommended)
st.markdown("## 💥 More to Explore")
for section in ["Top Rated", "Popular Picks", "Watch Again"]:
    st.markdown(f"### {section}")
    cols = st.columns(5)
    random.shuffle(placeholder_movies)
    for idx, movie in enumerate(placeholder_movies[:5]):
        with cols[idx]:
            st.image(movie["banner"], caption=movie["title"], use_column_width=True)
