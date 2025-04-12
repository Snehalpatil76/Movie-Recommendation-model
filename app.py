import streamlit as st
import pandas as pd
from surprise import SVD, Dataset, Reader
from surprise.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load datasets
movies = pd.read_csv("movies.csv")
ratings = pd.read_csv("ratings.csv")

# Preprocess ratings
reader = Reader(rating_scale=(0.5, 5))
data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)
trainset, testset = train_test_split(data, test_size=0.2)

# Train Collaborative Filtering Model
svd_model = SVD()
svd_model.fit(trainset)

# Content-Based Filtering setup-
tfidf = TfidfVectorizer(stop_words='english')
movies['overview'] = movies['overview'].fillna('')
tfidf_matrix = tfidf.fit_transform(movies['overview'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
indices = pd.Series(movies.index, index=movies['title']).drop_duplicates()

# Hybrid Recommender Function
def hybrid_recommendation(title, userId, top_n=10):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
    movie_indices = [i[0] for i in sim_scores]

    movie_ids = movies.iloc[movie_indices]['movieId']
    predictions = [svd_model.predict(userId, iid).est for iid in movie_ids]

    recommended = movies.iloc[movie_indices].copy()
    recommended['Predicted Rating'] = predictions
    return recommended[['title', 'Predicted Rating']].sort_values(by='Predicted Rating', ascending=False)

# Streamlit Interface
st.title("🎬 Hybrid Movie Recommendation System")
user_input = st.text_input("Enter a movie you like:")
user_id = st.number_input("Enter your user ID:", min_value=1, step=1)

if st.button("Recommend"):
    try:
        results = hybrid_recommendation(user_input, int(user_id))
        st.write("Top Recommendations:")
        st.table(results)
    except Exception as e:
        st.error(f"Error: {e}")
