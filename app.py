import streamlit as st
import requests

# Dummy recommendation function for example
def get_recommendations(movie_name):
    # Placeholder logic - you should use your actual model here
    return ["Inception", "Interstellar", "The Dark Knight", "Tenet", "Dunkirk"]

def fetch_poster_url(movie_title):
    api_key = "YOUR_ACTUAL_TMDB_API_KEY"  # Replace this with your key
    query = movie_title.replace(" ", "%20")
    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={query}"
    
    try:
        response = requests.get(url)
        data = response.json()
        if 'results' in data and data['results']:
            poster_path = data['results'][0].get('poster_path')
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"
    except Exception as e:
        print("API error:", e)
        
    return "https://via.placeholder.com/300x450?text=No+Image"


# Streamlit UI
st.set_page_config(layout="wide", page_title="Movie Recs")
st.markdown("""
    <style>
    body {
        background-color: #0b0c10;
        color: white;
    }
    .block-container {
        padding: 2rem 2rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='color:#ffffff;'>🍿 Movie Recommendations</h1>", unsafe_allow_html=True)

movie_name = st.text_input("", placeholder="Search your favorite movie...", label_visibility="collapsed")

if movie_name:
    recommended_movies = get_recommendations(movie_name)

    st.markdown("<h3 style='color:#ff4c4c;'>🎯 Recommended for You</h3>", unsafe_allow_html=True)
    cols = st.columns(len(recommended_movies))
    for i, movie in enumerate(recommended_movies):
        with cols[i]:
            poster = fetch_poster_url(movie)
            st.image(poster, caption=movie, use_container_width=True)

# Placeholder carousels
st.markdown("""
    <h2 style='color:#ffc107;'>🌟 More to Explore</h2>
    <h4 style='color:#ffffff;'>Top Rated ↩️</h4>
""", unsafe_allow_html=True)

top_rated = ["The Shawshank Redemption", "The Godfather", "The Dark Knight", "Forrest Gump", "Pulp Fiction"]
cols = st.columns(len(top_rated))
for i, movie in enumerate(top_rated):
    with cols[i]:
        poster = fetch_poster_url(movie)
        st.image(poster, caption=movie, use_container_width=True)

# You can add a 'Trending Now' or 'Popular on Streamlit' carousel similarly!
