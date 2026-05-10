import streamlit as st
import pickle
import pandas as pd
import requests
import ast
import os
import gdown

if not os.path.exists("similarity.pkl"):
    url = "https://drive.google.com/uc?id=16FIu7J_JaFgzDt4zUM-z-KOIVOkUt-J8"
    gdown.download(url, "similarity.pkl", quiet=False)

similarity = pickle.load(open('similarity.pkl', 'rb'))




st.set_page_config(
    page_title="Netflix Movie Recommender",
    layout="wide"
)



st.markdown("""
<style>

.main {
    background-color: #0E1117;
    color: white;
}

h1,h2,h3,h4 {
    color: white;
}

.stButton>button {
    background-color: red;
    color: white;
    border-radius: 10px;
    height: 50px;
    width: 100%;
    font-size: 18px;
}

</style>
""", unsafe_allow_html=True)



movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movies_data = pd.read_csv('tmdb_5000_movies.csv')
import pickle
import pandas as pd

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))



def convert(obj):
    genres = []

    try:
        for i in ast.literal_eval(obj):
            genres.append(i['name'])
    except:
        pass

    return genres

movies_data['genres'] = movies_data['genres'].apply(convert)



def fetch_poster(movie_id):

    api_key = "8265bd1679663a7ea12ac168da84d2e8"

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"

    try:
        data = requests.get(url)
        data = data.json()

        poster_path = data['poster_path']

        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path

        return full_path

    except:
        return "https://via.placeholder.com/500x750?text=No+Image"


def recommend(movie):

    movie_index = movies[movies['title'] == movie].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:11]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].id

        recommended_movies.append(
            movies.iloc[i[0]].title
        )

        recommended_posters.append(
            fetch_poster(movie_id)
        )

    return recommended_movies, recommended_posters

# =========================
# TITLE
# =========================

st.title("🎬 Netflix Style Movie Recommendation System")

st.write("Find movies by genre and get smart recommendations")

# =========================
# RECOMMENDATION SECTION
# =========================

st.header("🔍 Movie Recommendation")

movie_list = movies['title'].values

selected_movie = st.selectbox(
    "Search or select a movie",
    movie_list
)

if st.button("Recommend Movies"):

    names, posters = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.image(posters[0])
        st.write(names[0])

    with col2:
        st.image(posters[1])
        st.write(names[1])

    with col3:
        st.image(posters[2])
        st.write(names[2])

    with col4:
        st.image(posters[3])
        st.write(names[3])

    with col5:
        st.image(posters[4])
        st.write(names[4])

    col6, col7, col8, col9, col10 = st.columns(5)

    with col6:
        st.image(posters[5])
        st.write(names[5])

    with col7:
        st.image(posters[6])
        st.write(names[6])

    with col8:
        st.image(posters[7])
        st.write(names[7])

    with col9:
        st.image(posters[8])
        st.write(names[8])

    with col10:
        st.image(posters[9])
        st.write(names[9])

# =========================
# GENRE SECTION
# =========================

st.header("🎭 Browse Movies By Genre")

all_genres = []

for genre_list in movies_data['genres']:

    for genre in genre_list:

        all_genres.append(genre)

all_genres = sorted(list(set(all_genres)))

selected_genre = st.selectbox(
    "Choose Genre",
    all_genres
)

filtered_movies = movies_data[
    movies_data['genres'].apply(
        lambda x: selected_genre in x
    )
]

genre_cols = st.columns(5)

count = 0

for index, row in filtered_movies.head(15).iterrows():

    try:

        poster = fetch_poster(row['id'])

        with genre_cols[count % 5]:

            st.image(poster)
            st.write(row['title'])

        count += 1

    except:
        pass

# =========================
# NETFLIX STYLE CATEGORIES
# =========================

st.header("🔥 Popular Categories")

categories = [
    'Action',
    'Comedy',
    'Horror',
    'Romance',
    'Thriller'
]

for category in categories:

    st.subheader(category)

    category_movies = movies_data[
        movies_data['genres'].apply(
            lambda x: category in x
        )
    ]

    cols = st.columns(5)

    for idx, (_, row) in enumerate(category_movies.head(5).iterrows()):

        try:

            poster = fetch_poster(row['id'])

            with cols[idx]:

                st.image(poster)
                st.write(row['title'])

        except:
            pass
