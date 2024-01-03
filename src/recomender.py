import pandas as pd 
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import seaborn as sns
import os
import pickle

data = pd.read_csv(os.join.path(os.getcwd(),"metadata/imdb_movie_data_2023.csv"))
data.rename(columns={'Moive Name': 'Movie Name'}, inplace=True)
data["Movie Name"] = data["Movie Name"].str[1:]
data = data.fillna("NA")
indices = pd.Series(data.index, index=data['Movie Name']).drop_duplicates()
columns=['Cast','Director','Genre','Movie Name']
data[columns].isnull().values.any()

def get_important_features(data):
    important_features=[]
    for i in range (0,data.shape[0]):
        important_features.append(data['Movie Name'][i]+' '+data['Director'][i]+' '+data['Genre'][i]+' '+data['Cast'][i])
    return important_features

# creating a column to hold the combined strings
data['important_features']=get_important_features(data)

vectorizer  = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(data["important_features"])

cosine = cosine_similarity(tfidf_matrix, tfidf_matrix)

def get_recommendation(title, cosine=cosine):
    idx = indices[title]
    scores = sorted(list(cosine[idx]), reverse=True)[0:6]
    movie_indices = [list(cosine[idx]).index(x) for x in scores]
    movies = data["Movie Name"][movie_indices]
    dict = {"Movies": movies, "ID": movie_indices}
    final_df = pd.DataFrame(dict)
    return final_df


movie_list = data["Movie Name"]
movie_list_path = os.join.path(os.getcwd(), "src/movie_list.pkl")
cosine_path = os.join.path(os.getcwd(), "cosine.pkl")
pickle.dump(movie_list, open(movie_list, "wb"))
pickle.dump(cosine, open(cosine_path, "wb"))