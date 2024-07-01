import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=9fa4690ed731b579ef8ae1fcd8da01b6&language=en-US'.format(movie_id))
    data = response.json()

    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def get_movie_info(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=9fa4690ed731b579ef8ae1fcd8da01b6&language=en-US'.format(movie_id))
    data = response.json()

    return {
        'Release Date': data['release_date'],
        'Overview': data['overview']
    }

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    recommended_movies_info = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
        recommended_movies_info.append(get_movie_info(movie_id))

    return recommended_movies, recommended_movies_posters, recommended_movies_info

movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'What do you like?',
    movies['title'].values
)

if st.button('Show Recommendation'):
    with st.spinner('Fetching Recommendations...'):
        names, posters, info = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    for i, (name, poster, movie_info) in enumerate(zip(names, posters, info)):
        with globals()[f"col{i+1}"]:
            st.text(name)
            st.image(poster)
            st.write(f"Release Date: {movie_info['Release Date']}")
            st.write(f"Overview: {movie_info['Overview']}")

