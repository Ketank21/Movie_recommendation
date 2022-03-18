'''
root module of the recommender app
'''

from flask import Flask, request, render_template
from recommender import recommend_nmf, recommend_random,recommend_neighbors,recommend_popular
from utils import movies,ratings,df_mov_avg_cnt, search_title,movie_to_id,id_to_movie,get_movieId

#where we define our Flask object to be used to render our views
app = Flask(__name__) # __name__ defines this script as the root of our movieapp

# decorator that routes the function to a specified URL
@app.route('/')
def landing_page():
    '''
    User lands on this page and enters query
    '''
    return render_template('landing_page.html')

@app.route('/my-awesome-recommender/')
def recommender():
    '''
    queries accessed and transformed into recommendations
    '''
    print(request.args) # accesses the user query, prints in temrinal
    # example query for the .getlist method: ?q=star+wars&q=godfather&q=get+shorty
    print(request.args.getlist('q')) # accesses the user query as a list

    choice = request.args.get('choice')
    
    # string input received from the user of the website
    userquery = request.args.getlist('movie')
    userquery_to_movieId=get_movieId(userquery)

    # TODO: convert user input into moveIds
    # - option 1: assume that user knows the movieIds: convert strings to integers (Erkan)
    # - option 2: use fuzzy string to match user input with exact titles from the movies table (Tosin)
    

    if choice == 'Random':
        recs = recommend_random(userquery_to_movieId, k=5)
            
    elif choice == 'Tailored':
        recs = recommend_nmf(userquery_to_movieId,k=5)

    elif choice == 'people like you':
        recs = recommend_neighbors(userquery_to_movieId,k=5)
    elif choice == 'popular':
        recs = recommend_popular(userquery_to_movieId,k=5)
    

    # query must be a list of moveieIds
    
    # recs = recommend_random(userquery_to_movieId, k=3)
    return render_template('recommender.html', recs=recs, choice=choice)

# parameterized URL
@app.route('/movie/<int:movieId>')
def movie_info(movieId):
    '''
    page for individual movie information
    '''
    movie=movies.set_index('movieId').loc[movieId]
    return render_template('movie_info.html', movie=movie, movieId=movieId) 


if __name__ == '__main__':
    # debug = True restarts servers after edits and prints verbose errors in terminal
    app.run(debug=True)
