import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv('movies.csv')
    df['genres'] = df['genres'].fillna('')
    return df

movies = load_data()

# Compute similarity matrix
@st.cache_data
def compute_similarity(data):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(data['genres'])
    return linear_kernel(tfidf_matrix, tfidf_matrix)

cosine_sim = compute_similarity(movies)
indices = pd.Series(movies.index, index=movies['title']).drop_duplicates()

# Recommendation function
def get_recommendations(title, sim=cosine_sim, n=10):
    try:
        idx = indices[title]
        sim_scores = list(enumerate(sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:n+1]
        movie_indices = [i[0] for i in sim_scores]
        return movies.iloc[movie_indices]
    except KeyError:
        return pd.DataFrame()

# UI
st.title("🎬 Simple Movie Recommender")

selected_movie = st.selectbox("Select a movie:", sorted(movies['title'].unique()))

if st.button("Recommend"):
    st.write(f"Recommendations based on: **{selected_movie}**")
    results = get_recommendations(selected_movie)

    if not results.empty:
        for _, row in results.iterrows():
            st.image("https://via.placeholder.com/200x300.png?text=Poster", width=150)
            st.write(f"**{row['title']}**")
            st.caption(f"Genres: {row['genres']}")
            st.markdown("---")
    else:
        st.warning("No recommendations found.")
