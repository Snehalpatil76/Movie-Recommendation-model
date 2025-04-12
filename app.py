import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Load movies data
movies = pd.read_csv('movies.csv')

# Fill missing genre values
movies['genres'] = movies['genres'].fillna('')

# Use TF-IDF on the genres
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies['genres'])

# Compute cosine similarity
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# Create reverse mapping
indices = pd.Series(movies.index, index=movies['title']).drop_duplicates()

# Recommendation function
def get_recommendations(title, cosine_sim=cosine_sim):
    idx = indices.get(title)

    if idx is None:
        return ["Movie not found!"]

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]  # Get top 10 similar

    movie_indices = [i[0] for i in sim_scores]
    return movies['title'].iloc[movie_indices]

# Streamlit UI
st.title('Movie Recommender System (Based on Genre)')
movie_name = st.text_input("Enter a movie title")

if st.button("Recommend"):
    if movie_name:
        recommendations = get_recommendations(movie_name)
        st.subheader("Recommended Movies:")
        for movie in recommendations:
            st.write(movie)
    else:
        st.warning("Please enter a movie title.")
