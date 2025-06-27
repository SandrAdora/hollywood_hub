#!/usr/bin/env python
# coding: utf-8

# # -------- Application Layer communicates with the backend and frontend

# In[2]:


import requests

import numpy as np
import json
import os
import re
import numpy as np
import sys

# parent directory 
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# add parent directory to system path 
sys.path.append(parent_dir)

from helperFunctions import  img_url_extractor, extract_infos, load_image, save_image, available_actors, best_known_for_genre, average_rating_of_each_actor


# ------- Fast API URL ----------------

FASTAPI_URL_SWAGGER = "http://127.0.0.1:8000/docs" # Shows all Endpoints at once
FASTAPI_URL = "http://127.0.0.1:8000/" # root
FASTAPI_CELEBS_URL = "http://127.0.0.1:8000/most_popular_celebrities"
FASTAPI_MOVIES = "http://127.0.0.1:8000/movies"

"http://127.0.0.1:8000/actors/1" # <----- you can try out different numbers [1 - 50]
"http://127.0.0.1:8000/actor/1" # <----- you can try out different numbers [1 - 50]
"http://127.0.0.1:8000/award/1" # <----- you can try out different numbers [1 - 50]
"http://127.0.0.1:8000/movie/3" # <----- you can try out different numbers [1 - 50]



# ------- Celabrities data
csv_file = "data/actors_ids_names_birthdates.csv"


# ### --------------GET Methods -----------------

def display_all_actors():
    """Loads celebrities from FastAPI endpoint by making a request.
        processes their images, and returns a list of actor data.

    Args:
        None:
    Returns: 
        list (List): List of all available actors
    """
    res = requests.get(FASTAPI_CELEBS_URL)
    img_path = "data/images"   
    # Ensure the image folder exists
    if not os.path.exists(img_path):
        print(f"Path {img_path} does not exist.")
        return None
    best_known_for = ""
    lists_of_actors = []
    result = res.json()
    for actor in result:
        img_name = actor["name"].lower().replace(" ", "_")
        name = actor["name"]
        birthdate = actor["birthday"]
        best_known_for = best_known_for_genre(name)

        lists_of_actors.append({
            "name": name,
            "birthdate": birthdate,
            #"image": anvil.BlobMedia("image/JPEG", open(f"data/images/{img_name}.jpg", "rb").read()),
            "actor_genre": best_known_for
        })
    return lists_of_actors

# Keeps the uplink running (if needed)
#anvil.server.wait_forever()


# In[4]:



def all_time_movies(person: str):
    """This function returns all the movies an actor stared in 
    In addition it returns the average rating of each actor
    Parameter: 
        name (str): Full name of an actor

    Return: 
        movies (list): List of movies an actor stared in
        average (float): Average Rating number """
    list_of_movies = []
    """This function returns the list of all movies an actor stared in """
    img_folder = person.lower().replace(" ", "_")

    top_movies = []
    res = requests.get(FASTAPI_CELEBS_URL)
    actors = res.json()
    id = None
    for data in actors:
        if person.lower() == data["name"].lower():
            id = data["id"]
    movies = requests.get(f"http://127.0.0.1:8000/movie/{id}")
    if id is None:
        return []
    actor_movies = movies.json()
    i = 1
    for movie in actor_movies:

        title = movie["title"]
        img_name = re.sub(r'[\/:*?"<>|]', '_', title)
        img_name = img_name.replace(" ", "_")
        rating = movie["rating"]
        genre = movie["genre"]
        year = movie["year"]
        top_movies.append(
            {
            #"movie_image": anvil.BlobMedia("image/JPEG", open(f"data/images/movie_images_{img_folder}/{img_name}.jpg", "rb").read()),
            "movie_title": title,
            "movie_rating" : rating,
            "movie_genre": genre,
            "movie_year": year               
            }
        )
    return top_movies


# In[5]:

def actor_profile(name_input):
    """This Function returns the profile of a specific actor when full name is given
    It sends a request to the fastapi endpoints to retieve the data its needs from an actor

    Args:
        name (str): Full name of an actor
    Returns: 
        profile (list): List of an actor's achievments
    """
    list_of_profiles = []

    res = requests.get(FASTAPI_CELEBS_URL)
    actors = res.json()
    id = 0
    for data in actors:
        if name_input.lower() == data["name"].lower():
            id = data["id"]
    if id == 0:
        return []
    pros_res = requests.get(f"http://127.0.0.1:8000/actors/{id}")
    awards_res = requests.get(f"http://127.0.0.1:8000/award/{id}")
    awards = awards_res.json()
    profile = pros_res.json() 

    img_name = profile["name"].lower().replace(" ", "_")
    actor_name = profile["name"]
    birthdate = profile["birthday"]
    biography = profile["biography"]
    nominations = awards["nominations"]
    award_won = awards["award_won"]

    list_of_profiles.append(
        {
            "actor_name_profile": actor_name,
            "birthdate_profile": birthdate, 
            "biography": biography, 
            #"image_profile": anvil.BlobMedia("image/JPEG", open(f"data/images/{img_name}.jpg", "rb").read()),
            "nominations": nominations,
            "won": award_won,
            "average_rating" : round(average_rating_of_each_actor(actor_name), 2)
        }
    )
    return list_of_profiles





def get_actors_movies(person):
    """This function returns the list of all movies an actor stared in """
    img_folder = person.lower().replace(" ", "_")
    top_5_movies = []
    res = requests.get(FASTAPI_CELEBS_URL)
    if res.status_code != 200:
        print("Error: No connection possible")
        return None
    actors = res.json()
    id = None
    for data in actors:
        if person.lower() == data["name"].lower():
            id = data["id"]
    if id is None:
        return []
    movies = requests.get(f"http://127.0.0.1:8000/movie/{id}")
    actor_movies = movies.json()
    i = 1
    for movie in actor_movies:
        if i <= 5:
            title = movie["title"]
            img_name = re.sub(r'[\/:*?"<>|]', '_', title)
            img_name = img_name.replace(" ", "_")
            rating = movie["rating"]
            genre = movie["genre"]
            year = movie["year"]
            top_5_movies.append(
                {
                #"movie_image": anvil.BlobMedia("image/JPEG", open(f"data/images/movie_images_{img_folder}/{img_name}.jpg", "rb").read()),
                "movie_title": title,
                "movie_rating" : rating,
                "movie_genre": genre,
                "movie_year": year               
                }
            )
            i += 1
    return top_5_movies


def get_actor_awards(name):
    """This function returns a list of all awards an actor won"""
    res = requests.get("http://127.0.0.1:8000/most_popular_celebrities")
    if res.status_code != 200:
        return None

    actors = res.json()
    id = None
    for data in actors:
        if data["name"].lower() == name.lower():
            id = data["id"]
    if id == None:
        return []
    res_award = requests.get(f"http://127.0.0.1:8000/award/{id}") 
    awards_data = res_award.json()
    list_of_awards = []
    awards = awards_data["award_name"]
    years = awards_data["year"]

    for award, year in zip([awards[i] for i in range(len(awards))], [years[k] for k in range(len(years))]):
        list_of_awards.append(
            {
                "award_name": award, 
                "award_year": year
            }
        )
    return list_of_awards

