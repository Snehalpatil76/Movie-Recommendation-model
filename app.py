import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Page Config
st.set_page_config(
    page_title="🎬 Netflix-Style Movie Recommender",
    page_icon="🍿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load the data
@st.cache_data
def load_data():
    movies = pd.read_csv('movies.csv')
    movies['genres'] = movies['genres'].fillna('')
    return movies

movies = load_data()

# Placeholder image fetcher
def fetch_poster(movie_title):
    return "https://via.placeholder.com/500x750?text=Movie+Poster"

# TF-IDF Vectorization
@st.cache_data
def create_similarity_matrix(movies_data):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(movies_data['genres'])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    return cosine_sim

cosine_sim = create_similarity_matrix(movies)

# Reverse mapping
indices = pd.Series(movies.index, index=movies['title']).drop_duplicates()

# Recommendation Function
def get_recommendations(title, cosine_sim=cosine_sim, n=10):
    try:
        idx = indices[title]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:n+1]
        movie_indices = [i[0] for i in sim_scores]
        recommendations = movies['title'].iloc[movie_indices]
        return recommendations
    except KeyError:
        return pd.Series([])

# ---------- UI Section ------------

# Custom CSS for Netflix-style UI
st.markdown("""<style>
    .stApp { background-color: #141414; color: #FFFFFF; }
    h1, h2, h3 { font-family: 'Netflix Sans', 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .netflix-header { color: #E50914; font-weight: bold; font-size: 3rem; margin-bottom: 0; padding-bottom: 0; }
    .netflix-subheader { color: #CCCCCC; font-size: 1.2rem; margin-top: 0; padding-top: 0; margin-bottom: 2rem; }
    .stSelectbox > div > div { background-color: #333333; color: white; border-radius: 5px; }
    .stSelectbox label { color: #CCCCCC; font-size: 1.2rem; }
    .netflix-button {
        background-color: #E50914; color: white; font-weight: bold;
        padding: 0.7em 2em; font-size: 1.2rem; border-radius: 4px;
        border: none; cursor: pointer; transition: all 0.3s; width: 100%;
        margin-top: 10px;
    }
    .netflix-button:hover {
        background-color: #F40612; transform: scale(1.02);
    }
    .movie-container {
        display: flex; flex-wrap: wrap; gap: 16px;
        justify-content: center; margin-top: 30px;
    }
    .movie-card {
        background-color: #181818; border-radius: 4px;
        overflow: hidden; transition: transform 0.3s ease;
        width: 220px; margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.4);
    }
    .movie-card:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 16px rgba(0,0,0,0.5);
    }
    .movie-poster {
        width: 100%; height: 330px; object-fit: cover;
    }
    .movie-title {
        padding: 12px; font-weight: bold;
        font-size: 1rem; white-space: nowrap;
        overflow: hidden; text-overflow: ellipsis;
        text-align: center;
    }
    .feature-container {
        position: relative; margin-bottom: 40px;
        border-radius: 8px; overflow: hidden;
    }
    .feature-image {
        width: 100%; height: 400px; object-fit: cover; opacity: 0.7;
    }
    .feature-overlay {
        position: absolute; bottom: 0; left: 0; right: 0;
        padding: 30px;
        background: linear-gradient(transparent, rgba(0,0,0,0.8) 40%, #000000);
    }
    .feature-title {
        font-size: 2.5rem; margin-bottom: 10px;
    }
    .genre-pill {
        display: inline-block;
        background-color: rgba(255,255,255,0.2);
        padding: 5px 15px;
        border-radius: 20px;
        margin-right: 10px;
        margin-bottom: 10px;
        font-size: 0.9rem;
    }
    .section-divider {
        height: 30px;
    }
</style>""", unsafe_allow_html=True)

# Header
st.markdown("<h1 class='netflix-header'>MOVIEFLIX</h1>", unsafe_allow_html=True)
st.markdown("<p class='netflix-subheader'>Find your next favorite movie with AI-powered recommendations</p>", unsafe_allow_html=True)

# Movie Selector
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    movie_name = st.selectbox("Search for a movie:", sorted(movies['title'].unique()))
    
    if st.button("Get Recommendations", key="recommend_button"):
        with st.spinner("Finding movies you'll love..."):
            selected_movie = movies[movies['title'] == movie_name]
            genres = selected_movie['genres'].iloc[0] if not selected_movie.empty else ""
            genres_list = [g.strip() for g in genres.split("|")] if genres else []

            # Featured movie section
            st.markdown("### Featured Movie")
            poster_url = fetch_poster(movie_name)

            feature_html = f"""
            <div class="feature-container">
                <img src="{poster_url}" class="feature-image">
                <div class="feature-overlay">
                    <div class="feature-title">{movie_name}</div>
                    <div class="feature-genres">
                        {"".join([f'<span class="genre-pill">{genre}</span>' for genre in genres_list])}
                    </div>
                </div>
            </div>
            """
            st.markdown(feature_html, unsafe_allow_html=True)

            recommendations = get_recommendations(movie_name)

            if not recommendations.empty:
                st.markdown("### Movies You Might Like")
                all_cards_html = '<div class="movie-container">'
                for rec in recommendations:
                    poster = fetch_poster(rec)
                    card_html = f"""
                    <div class="movie-card">
                        <img src="{poster}" class="movie-poster">
                        <div class="movie-title">{rec}</div>
                    </div>
                    """
                    all_cards_html += card_html
                all_cards_html += '</div>'
                st.markdown(all_cards_html, unsafe_allow_html=True)
            else:
                st.error("Sorry, we couldn't find recommendations for this movie.")

# Footer
st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color: #999; padding: 20px;">
    <p>© 2025 MovieFlix | Powered by AI Recommendations</p>
</div>
""", unsafe_allow_html=True)
