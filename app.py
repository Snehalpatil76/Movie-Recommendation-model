import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Load your data (make sure it's in your GitHub repo too)
movies = pd.read_csv('movies.csv')

# Vectorize the 'overview' column
tfidf = TfidfVectorizer(stop_words='english')
movies['overview'] = movies['overview'].fillna('')
tfidf_matrix = tfidf.fit_transform(movies['overview'])

# Compute cosine similarity
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# Build index mapping
indices = pd.Series(movies.index, index=movies['title']).drop_duplicates()

# Recommendation function
def get_recommendations(title):
    idx = indices.get(title)
    if idx is None:
        return ["Movie not found. Try another title."]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return movies['title'].iloc[movie_indices].tolist()

# Streamlit UI
st.title("🎬 Movie Recommender System (Content-Based)")

user_input = st.text_input("Enter a movie title:", "The Dark Knight")
if user_input:
    recommendations = get_recommendations(user_input)
    st.write("Recommended Movies:")
    for rec in recommendations:
        st.write(f"- {rec}")
