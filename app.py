import pandas as pd
import pickle
import streamlit as st
import os
def get_recommendation(title, movies):
    idx = list(movies).index(title)
    scores = sorted(list(cosine[idx]), reverse=True)[0:6]
    movie_indices = [list(cosine[idx]).index(x) for x in scores]
    movies = movies[movie_indices]
    dict = {"Movies": movies, "ID": movie_indices}
    final_df = pd.DataFrame(dict)
    return movies[1:]
page_bg_img = '''
<style>
      .stApp {
  background-image: url("https://e1.pxfuel.com/desktop-wallpaper/760/665/desktop-wallpaper-hollywood-news-hollywood-2022-movies-poster.jpg");
  background-size: cover;
}
.stSelectbox {
            background-color:white; /* Replace with the desired background color */
            color:white; /* Replace with the desired text color */
        }
.stsubheader {
            background-color:white;
            color:white;
}
</style>
'''
    



st.markdown(page_bg_img, unsafe_allow_html=True)


st.markdown('<p style="font-size: 40px; color:white;">Movie Recommendor</p>', unsafe_allow_html=True)
movie_list_path = os.path.join(os.getcwd(),'src/movie_list.pkl')
cosine_path = os.path.join(os.getcwd(), 'src/cosine.pkl')
movies = pickle.load(open(movie_list_path,'rb'))
cosine = pickle.load(open(cosine_path,'rb'))
# indices = pd.Series(movies.index).drop_duplicates()
selected_movie = st.selectbox(
    '## **Type or select a movie from the dropdown**',
    movies.values
)
if st.button('Show Recommendation'):
    recommended_movie_names = get_recommendation(selected_movie, movies)
    for n, i in enumerate(recommended_movie_names):
        movie = str(n+1)+". "+i
        st.markdown(f'<p style="font-size: 20px; color:white;">{movie}</p>', unsafe_allow_html=True)