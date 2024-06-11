# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 11:03:45 2024

@author: abhis
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 10:54:58 2024

@author: abhis
"""

import requests
import time
import re
import os
import pandas as pd
import json
def getImage(movieId):
    MOVIE_API_TOKEN="eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxYTIzZGFiYzNlOGYyMTM0NWQ2ZTFlZmI4YjQ3ZGI0OCIsInN1YiI6IjY2Mjk2ZDQyYmJlMWRkMDE2NWE5YzAyNCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.V60AIIC8NHwo2C7XrWBooxUHWyPClFMIyImJn34Rb44"

    '''
    Get Images using the TMDB API
    '''
    
    url = f"https://api.themoviedb.org/3/movie/{movieId}/images"    
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer "+MOVIE_API_TOKEN
    }    
    response = requests.get(url, headers=headers)    
    vals = json.loads(response.text)['posters']    
    vals = ['http://image.tmdb.org/t/p/w185/' + x['file_path'] if x['iso_639_1']=='en' else 'http://image.tmdb.org/t/p/w185/' + x['file_path'] for x in vals]
    return vals[0]

wd2 = r'C:\Users\abhis\.Neo4jDesktop\relate-data\dbmss\dbms-270e66cc-c52d-46b5-9148-c8e81def25cf\import\\'

def download_poster(downloaded_image_dir, title, label, poster_path,id1):
    
    if not os.path.exists(downloaded_image_dir):
        os.makedirs(downloaded_image_dir)
        
    if not os.path.exists(downloaded_image_dir+'/'+label):
        os.makedirs(downloaded_image_dir+'/'+label)

    imgUrl = getImage(id1)#'http://image.tmdb.org/t/p/w185/' + poster_path

    local_filename = re.sub(r'\W+', ' ', title).lower().strip().replace(" ", "-") + '.jpg'

    try:
        session = requests.Session()
        r = session.get(imgUrl, stream=True, verify=False)
        with open(r"C:\Users\abhis\Desktop\NEU\INFO7375 ST Prompt Engineering & AI\Assignment4\someImages"+'/'+local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                f.write(chunk)
    except:
        print('PROBLEM downloading', title,label,poster_path,imgUrl)
    
    time.sleep(1)

# download image by iterate pandas
df_movies = pd.read_csv(wd2+"movies_metadata_clean.csv").sort_values('budget',ascending=False)    
for index, row in df_movies.head(10).iterrows():
    download_poster(
        'images_movies_genre',
        str(row['title']),
        str("_".join([x['name'] for x in eval(row['genres'])])),
        row['poster_path'],row['id']
    )