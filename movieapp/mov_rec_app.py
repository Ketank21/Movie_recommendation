import streamlit as st
import pandas as pd
from recommender import recommend_neighbors,recommend_nmf,recommend_popular,recommend_random
from utils import movies, ratings,search_title,id_to_movie,get_movieId
from utils import model_nmf,model_knn
from apikey import omdbapikey
import requests

nav_rad=st.sidebar.radio("Contents",["Home","References"])
if nav_rad=="Home":
    #Add text elemnents
    st.title(" Movie Recommender App")
    st.markdown("### Please enter 5 of your favorite movies so that we can curate a list of movie recommendations for you ###")

    movie1 = st.selectbox('Type/Select your first movie here',movies['title'].unique())

    movie2 = st.selectbox('Type/Select your second movie here',movies['title'].unique())

    movie3 = st.selectbox('Type/Select your third movie here',movies['title'].unique())

    movie4 = st.selectbox('Type/Select your fourth movie here',movies['title'].unique())

    movie5 = st.selectbox('Type/Select your fifth movie here',movies['title'].unique())

    st.subheader("Select the type of recommendation")
    reco_type = st.radio('',["Random","Tailored to you","People like you","Popular"])

    user_list = [movie1,movie2,movie3,movie4,movie5]
    user_list_to_movieId = get_movieId(user_list)

    if st.button(' Recommendations'):
            if reco_type == 'Random':
                recs = recommend_random(user_list_to_movieId, k=5)
                        
            if reco_type == 'Tailored to you':
                recs = recommend_nmf(user_list_to_movieId,k=5)

            if reco_type == 'People like you':
                recs = recommend_neighbors(user_list_to_movieId,k=5)

            if reco_type == 'Popular':
                recs = recommend_popular(user_list_to_movieId,k=5)

            rec_movies =[]
            for index in recs.index:
                st.button(recs.loc[index][0])

            
    st.markdown("### Want to explore any of these movies? type it below ###")
    title =st.selectbox('',movies['title'].unique())     


    moviename = title[:-6]
    cleaner_name=moviename.split(',')
    actual_search_name =cleaner_name[0]
    url = f"http://www.omdbapi.com/?t={str(actual_search_name)}&apikey={omdbapikey}"
    re = requests.get(url)
    if re: 
            re=re.json()
            col1,col2=st.columns([1,2])
            with col1:
                try:
                    st.image(re['Poster'])
                except:
                    st.error ("No poster :-/")
            with col2:
                try:
                    st.subheader(re['Title'])
                except:
                    st.error (" No title found :-/")
                try:
                    st.caption(f"Genre: {re['Genre']} Year: {re['Year']} ")
                except:
                    st.error ("No Genre found :-/")

                try:
                    st.write(re['Plot'])
                except:
                    st.error("No plot Found")
                try:
                    st.text(f"Rating: {re['imdbRating']} ")
                except:
                    st.error(" No Ratings Found :-/")
                try:
                    st.progress(float(re['imdbRating'])/10)
                except:
                    st.error(" No progress bar created :-/")
                    st.error(" You should look for some other movie :-)")

    else:
        st.error("no info about movie with that title! Sorry :-/")
if nav_rad =="References":
    st.markdown(""" 
- ### References ###

    - Spiced Academy Movie recommender project: 
      This is a basis for the work and pretty much my attempt of this 
      project we learnt in Spiced Academy, Stuttgart.

      https://www.spiced-academy.com/en

    - Youtube video ->A Movie Search App with Streamlit | Beginner Streamlit Project

      https://www.youtube.com/watch?v=az2WnfmqOwo
      
    - A movie Database with an extremely easy to use API.

      http://www.omdbapi.com/

- ### About me: ###
    - www.linkedin.com/in/ketankm85

     
     
 """)

