import streamlit as st
import requests
import streamlit.components.v1 as components
from database import load_movies

# Load movie list
try:
    movies_df = load_movies()  # This should return a DataFrame
    if movies_df.empty:
        st.error("No movies found in the database.")
        st.stop()
except Exception as e:
    st.error(f"Error loading movie list: {e}")
    st.stop()

# Prepare movie titles and IDs
movies_dict = {row['title']: row['id'] for _, row in movies_df.iterrows()}

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    except requests.RequestException as e:
        st.error(f"Error fetching poster: {e}")
    return None

def fetch_recommendations(movie_title):
    try:
        # Replace with your actual Flask API URL
        response = requests.get(f'http://127.0.0.1:5000/recommend?movie={movie_title}')
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json().get('recommendations', [])
    except requests.RequestException as e:
        st.error(f"Error fetching recommendations: {e}")
    return []

st.header("Movie Recommender System")

# Example carousel component usage (assuming correct implementation)
imageCarouselComponent = components.declare_component("image-carousel-component", path="frontend/public")

# Replace with your dynamic image URLs
imageUrls = [fetch_poster(movie_id) for movie_id in [1632, 299536, 17455, 2830, 429422, 9722, 13972, 240, 155, 598, 914, 255709, 572154]]
imageUrls = [url for url in imageUrls if url is not None]  # Filter out None values
imageCarouselComponent(imageUrls=imageUrls, height=200)

selectvalue = st.selectbox("Pick movie from dropdown", list(movies_dict.keys()))

if st.button("Show Recommend"):
    recommendations = fetch_recommendations(selectvalue)
    if recommendations:
        cols = st.columns(5)
        for i, movie in enumerate(recommendations[:5]):
            if i < 5:
                movie_id = movies_dict.get(movie)
                poster_url = fetch_poster(movie_id) if movie_id else None
                with cols[i]:
                    st.text(movie)
                    if poster_url:
                        st.image(poster_url)
                    else:
                        st.text("Poster not available")
    else:
        st.error("No recommendations found")
