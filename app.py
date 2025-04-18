import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Page Config
st.set_page_config(
    page_title="🎬 Movie Recommender",
    page_icon="🍿",
    layout="wide",
    initial_sidebar_state="auto"
)

# Load the data
@st.cache_data
def load_data():
    df = pd.read_csv("movies.csv")
    df['genres'] = df['genres'].fillna('')
    return df

movies = load_data()

# TF-IDF and cosine similarity
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies['genres'])
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# Mapping of indices
indices = pd.Series(movies.index, index=movies['title']).drop_duplicates()

# Recommendation function
def get_recommendations(title, cosine_sim=cosine_sim):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return movies['title'].iloc[movie_indices]

# Custom Styling
st.markdown("""
    <style>
    body {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    .stApp {
        background-color: #0E1117;
    }
    .stSelectbox label {
        color: #FAFAFA;
        font-size: 20px;
    }
    .stButton>button {
        background-color: #E50914;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.5em 1em;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #F40612;
        transform: scale(1.02);
    }
    </style>
""", unsafe_allow_html=True)

# UI Title
st.markdown("<h1 style='text-align: center; color: #E50914;'>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #FAFAFA;'>Get Top 10 Recommendations Based on Genre Similarity 🍿</h4>", unsafe_allow_html=True)
st.write("")

# Movie selector in center
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    movie_name = st.selectbox("Choose a movie to get recommendations:", sorted(movies['title'].unique()))

# Recommend Button
col_center = st.columns([3, 2, 3])[1]
with col_center:
    if st.button("🎯 Recommend Movies"):
        recommendations = get_recommendations(movie_name)
        st.success("Here are your top 10 similar movies:")
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"**{i}. {rec}**")
