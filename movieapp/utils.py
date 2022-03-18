'''
import data here and have utility functions that could help
'''
import pandas as pd
import pickle
from psutil import users
from thefuzz import fuzz, process
from apikey import omdbapikey
import streamlit as st
import requests

movies =pd.read_csv('./data/ml-latest-small/movies.csv')
# print(movies.head())
ratings = pd.read_csv('./data/ml-latest-small/ratings.csv')
# print(ratings.head())
df_mov_avg_cnt=pd.read_csv('./data/ml-latest-small/movies_avg_cnt.csv')
with open('./models/nmf_recommender.pkl', 'rb') as file:
    model_nmf = pickle.load(file)
with open('./models/distance_recommender.pkl', 'rb') as file:
    model_knn = pickle.load(file)

movie_name_list=df_mov_avg_cnt['title'].to_list()

def search_title(search_query):
    """
    Uses fuzzy string matching to search for a movie titles in a dict of titles
    returns: a tuple (title, score, movieId)
    """
    movie_titles=[]
    for query in search_query:
        moviename=process.extract(query,movie_name_list,limit=1)
        movie_title=moviename[0][0]
        movie_titles.append(movie_title)

    return movie_titles


def movie_to_id(movie_titles):
    '''
    converts movie title to id for use in algorithms
    '''
    movieId_list=df_mov_avg_cnt.set_index('title').loc[movie_titles]['movieId'].to_list()
    return movieId_list


def id_to_movie(movieId):
    '''
    converts movie Id to title
    '''


def get_movieId(userquery):
    moviename=search_title(userquery)
    query=movie_to_id(moviename)
    return query

def get_movieId_st(user_list):
    query_st =movie_to_id(user_list)
    return query_st



    
