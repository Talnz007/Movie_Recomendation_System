import os
import streamlit as st
import requests
import streamlit.components.v1 as components
from database import fetch_movie_by_title, fetch_similar_movies, fetch_all_movie_titles
from dotenv import load_dotenv

load_dotenv()
TMDB_API = os.getenv('TMDB_API_KEY')

# Prepare movie titles and IDs
movies_dict = {}
try:
    # Dynamically fetch movie titles from the database
    movie_titles = fetch_all_movie_titles()
    if movie_titles:
        movies_dict = {movie['title']: movie['id'] for movie in movie_titles}
    else:
        st.error("No movies found in the database.")
        st.stop()
except Exception as e:
    st.error(f"Error loading movie list: {e}")
    st.stop()


def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API}"
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
        # Fetch movie data from the database
        movie_data = fetch_movie_by_title(movie_title)
        if movie_data:
            recommendations = fetch_similar_movies(movie_data["embedding"])
            return recommendations
        else:
            st.error("Movie not found.")
            return []
    except Exception as e:
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
                        # Store the play URL with the poster
                        tmdb_id = movie_id
                        play_url = f"https://multiembed.mov/?video_id={tmdb_id}&tmdb=1" if tmdb_id else None

                        # Create a clickable image that opens the movie
                        if play_url:
                            # Use HTML to create a clickable image that opens in a new tab
                            st.markdown(f'''
                                <a href="{play_url}" target="_blank">
                                    <img src="{poster_url}" style="width:100%; cursor:pointer;" />
                                </a>
                            ''', unsafe_allow_html=True)
                        else:
                            # If no play URL, just show the poster
                            st.image(poster_url)
                    else:
                        st.text("Poster not available")
    else:
        st.error("No recommendations found")