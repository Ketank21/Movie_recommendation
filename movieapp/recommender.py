"""
contains various implementations for recommending movies
"""

import pandas as pd
import numpy as np
from utils import movies
from utils import movies,ratings,df_mov_avg_cnt, search_title,movie_to_id,id_to_movie,get_movieId
from utils import model_nmf,model_knn
from scipy.sparse import csr_matrix # creating the matrix (filling in 0 when there is no entry)
from sklearn.decomposition import NMF #  Non matrix factorization for Recommneder system


def recommend_random(query, k=5):
    """
    Recommends a list of k random movie ids
    """
    movies_rand =movies[~movies['movieId'].isin(query)] # drops all movies in the query 
    rand_list=movies_rand.sample(k)['movieId'].to_list()
    rand_movie_title_list=[]
    for list in rand_list:
        movie_title = movies.loc[movies['movieId']==list,'title'].values[0]
        rand_movie_title_list.append(movie_title)
    df_rand_recommended=pd.DataFrame(rand_movie_title_list,rand_list)

    return df_rand_recommended


def recommend_popular(query, k=5):
    """
    Recommend a list of k movie ids that are from 40 most popular
    """ 
    df_popular=df_mov_avg_cnt[~df_mov_avg_cnt['movieId'].isin(query)]
    popular=df_popular.sort_values('popular',ascending=False)['movieId'].head(40).to_list()
    rand_popular = np.random.randint(40,size =(1,5))
    pop_movieId_list=[]
    for rand_nu in range(len(rand_popular[0])):
        pop_id = popular[rand_popular[0][rand_nu]]
        pop_movieId_list.append(pop_id)
    pop_movietitle_list=[]
    for list_pop in pop_movieId_list:
        movie_title_pop=movies.loc[movies['movieId']==list_pop,'title'].values[0]
        pop_movietitle_list.append(movie_title_pop)

    df_pop_recommended =pd.DataFrame(pop_movietitle_list,pop_movieId_list)
    
    return df_pop_recommended


def recommend_nmf(query, k=5):
    """
    Recommend a list of k movie ids based on a trained NMF model
    """
     # 1. candiate generation
    # user_query = disney_movies
   
    # construct a user vector
    user_vec=np.repeat(0,193610)
    user_vec[query]=5
   
    # 2. scoring
    model = model_nmf
    scores=model.inverse_transform(model.transform([user_vec])) # calculate the score with the NMF model    
    
    # 3. ranking
    scores =pd.Series(scores[0])
    scores[query]=0 # set zero score to movies allready seen by the user
    scores=scores.sort_values(ascending=False)  
    
    # return the top-k highst rated movie ids or titles
    recommendations= scores.head(k).index
    moiveId_r=[]
    movieId_t=[]
    for recs in range(len(recommendations)):
        movieId_r_Var = recommendations[recs]
        movieId_t_Var= movies.set_index('movieId').loc[movieId_r_Var]['title']
        moiveId_r.append(movieId_r_Var)
        movieId_t.append(movieId_t_Var)
    
    df_nmf=pd.DataFrame(movieId_t,moiveId_r)
    
    return df_nmf


def recommend_neighbors(query, k=5):
    """
    Recommend a list of k movie ids based on the most similar users
    """
    # 1. candiate generation
    user_vec=np.repeat(0,193610)
    user_vec[query]=5 # construct a user vector
    # calculates the distances to all other users in the data!
    distances, userIds = model_knn.kneighbors(
    X=[user_vec], 
    n_neighbors=10, 
    return_distance=True
    )

    # sklearn returns a list of predictions - extract the first and only value of the list
    distances = distances[0]
    userIds = userIds[0]
       
    # 2. scoring
    # find n neighbors
    neighborhood =ratings.loc[ratings['userId'].isin(userIds)]

    scores=neighborhood.groupby('movieId')['rating'].sum()
    # calculate their average rating
    
    
    # 3. ranking
    # filter out movies allready seen by the user
    # give a zero score to movies the user has allready seen
    scores.loc[scores.index.isin(query)]=0
    scores = scores.sort_values(ascending=False)
    recommendations=scores.head(k).index
    
    # return the top-k highst rated movie ids or titles
    moiveId_r=[]
    movieId_t=[]
    for recs in range(len(recommendations)):
        movieId_r_Var = recommendations[recs]
        movieId_t_Var= movies.set_index('movieId').loc[movieId_r_Var]['title']
        moiveId_r.append(movieId_r_Var)
        movieId_t.append(movieId_t_Var)
    
    df_knn=pd.DataFrame(movieId_t,moiveId_r)
    return df_knn




# # list of liked movies
# query = [1, 34, 56, 21]
# print(recommend_random(query))
