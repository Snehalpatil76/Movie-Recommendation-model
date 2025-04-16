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
movies = pd.read_csv('movies.csv')

# Fill NA values in genres
movies['genres'] = movies['genres'].fillna('')

# TF-IDF Vectorization on genres
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies['genres'])

# Compute cosine similarity
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# Create reverse mapping of indices and movie titles
indices = pd.Series(movies.index, index=movies['title']).drop_duplicates()

# Recommendation Function
def get_recommendations(title, cosine_sim=cosine_sim):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:11]  # Skip itself, top 10
    movie_indices = [i[0] for i in sim_scores]
    return movies['title'].iloc[movie_indices]
