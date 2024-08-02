import streamlit as st
import os
import git
import pickle
import requests
import streamlit.components.v1 as components

# Load token from Streamlit secrets
token = st.secrets["github"]["token"]
repo_url = f"https://{token}:x-oauth-basic@github.com/Talnz007/Movie_Recomendation_System.git"

# Clone the repository
repo_path = 'repo_path'
if not os.path.exists(repo_path):
    git.Repo.clone_from(repo_url, repo_path)
else:
    repo = git.Repo(repo_path)
    repo.remotes.origin.pull()

# Load data
movies = pickle.load(open(os.path.join(repo_path, "movies_list.pkl"), 'rb'))
similarity = pickle.load(open(os.path.join(repo_path, "similarity.pkl"), 'rb'))

movie_list = movies['title'].values

st.header("Movie Recommendation System")

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return full_path

imageCarouselComponent = components.declare_component("image-carousel-component", path="frontend/public")

imageUrls = [
    fetch_poster(1632),
    fetch_poster(299536),
    fetch_poster(17455),
    fetch_poster(2830),
    fetch_poster(429422),
    fetch_poster(9722),
    fetch_poster(13972),
    fetch_poster(240),
    fetch_poster(155),
    fetch_poster(598),
    fetch_poster(914),
    fetch_poster(255709),
    fetch_poster(572154)
]

imageCarouselComponent(imageUrls=imageUrls, height=200)
selectvalue = st.selectbox("Pick movie from dropdown", movie_list)

def recommendations(movie):
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommend_movie = []
    recommend_poster = []
    for i in distance[1:6]:
        movies_id = movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movies_id))
    return recommend_movie, recommend_poster

if st.button("Show Recommendation"):
    movie_name, recommend_poster = recommendations(selectvalue)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(movie_name[0])
        st.image(recommend_poster[0])
    with col2:
        st.text(movie_name[1])
        st.image(recommend_poster[1])
    with col3:
        st.text(movie_name[2])
        st.image(recommend_poster[2])
    with col4:
        st.text(movie_name[3])
        st.image(recommend_poster[3])
    with col5:
        st.text(movie_name[4])
        st.image(recommend_poster[4])
