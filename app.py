import streamlit as st
import pandas as pd
from fuzzywuzzy import process

# Load the movie dataset
movies_df = pd.read_csv('movies_metadata.csv')  # Make sure this is the correct dataset

# Extract the list of movie titles
movie_titles = movies_df['title'].tolist()

# Function to suggest movie names based on user input
def get_movie_suggestions(user_input, movie_titles):
    user_input = user_input.lower()  # Convert to lowercase
    suggestions = process.extract(user_input, movie_titles, limit=5)  # Get top 5 matches
    return [suggestion[0] for suggestion in suggestions]

# Streamlit UI
st.set_page_config(page_title="Movie Recommendation System", page_icon="🎬", layout="wide")
st.markdown("""
    <style>
        .header {
            text-align: center;
            color: white;
            font-size: 3rem;
            font-family: 'Arial', sans-serif;
        }
        .title {
            color: #00BFFF;
            font-size: 2.5rem;
        }
        .description {
            color: #A9A9A9;
            font-size: 1.2rem;
            margin-bottom: 20px;
        }
        .movie-suggestions {
            display: flex;
            overflow-x: scroll;
            gap: 10px;
            padding: 10px 0;
        }
        .movie-card {
            background-color: #1c1c1c;
            border-radius: 10px;
            padding: 20px;
            color: white;
            width: 150px;
            text-align: center;
        }
        .movie-card img {
            width: 100%;
            border-radius: 10px;
        }
        .btn {
            background-color: #00BFFF;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
        }
        .btn:hover {
            background-color: #1e90ff;
        }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("<h1 class='header'>🎬 Movie Recommendation System</h1>", unsafe_allow_html=True)
st.markdown("<p class='description'>Start typing a movie name below to get recommendations!</p>", unsafe_allow_html=True)

# User input for movie search
user_input = st.text_input("Movie Name", placeholder="Enter a movie title...")

if user_input:
    # Get movie suggestions
    suggestions = get_movie_suggestions(user_input, movie_titles)
    st.markdown("<p class='title'>Did you mean one of these movies?</p>", unsafe_allow_html=True)

    # Display movie suggestions in a carousel-like format
    st.markdown('<div class="movie-suggestions">', unsafe_allow_html=True)
    for movie in suggestions:
        # Create a movie card for each suggestion
        st.markdown(f"""
            <div class="movie-card">
                <img src="https://via.placeholder.com/150x200?text={movie}" alt="{movie}" />
                <p>{movie}</p>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Movie selection dropdown
    selected_movie = st.selectbox("Select a movie from the suggestions:", suggestions)

    if selected_movie:
        st.write(f"You selected: {selected_movie}")
        # Here, you'd normally call your recommendation function based on selected_movie
        # For now, let's just show a placeholder
        st.write("Fetching recommendations based on this movie...")

else:
    st.write("Start typing a movie name to get suggestions.")
