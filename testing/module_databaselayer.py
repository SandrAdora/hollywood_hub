#!/usr/bin/env python
# coding: utf-8

# # --- Setting up the Backend of the Hollywoodhub Application 

# ##---------------------------- Importing important Modules ----------------------------

# In[1]:


# Listing all files in my current directory
import os
import sys
print(os.listdir())
# parent directory 
# parent directory 
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# add parent directory to system path 
sys.path.append(parent_dir)

# In[2]:


import json
import csv
import uvicorn
import anvil.server
import nest_asyncio
import asyncio


from fastapi import FastAPI , Depends, HTTPException, Request
from helperFunctions import extract_infos, create_actor_csv, get_actors_best_known_for_movies

from typing import List
from models import ActorCreate, ActorCreateResponse, AwardCreate, AwardCreateResponse, MovieCreate, MovieResponse, ActorMovieResponse
from models import UpdateGenre
from flask import Flask, render_template
from fastapi.middleware.cors import CORSMiddleware


# --------------------------- For setting up api and database ----------------------------
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session, joinedload
from databaseModels import Actor, Award, Movie 


# ---------- Setting up Backend--------------
fastapi_app = FastAPI()

# ----- Database Setup -----
    # DATABASE_URL = "sqlite:///celeb.db"
    # engine = create_engine(DATABASE_URL)
    # SessionLocal = sessionmaker(expire_on_commit=False, autoflush=False, bind=engine)
# ----- Database Setup -----

def get_db():
    DATABASE_URL = "sqlite:///celeb.db"
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(expire_on_commit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db # return value and pause function used on api endpoint
    finally:
        db.close()  

# ------- Celabrities data -----------------------
csv_file = "data/actors_ids_names_birthdates.csv"


# ## ----------------------  Post Functions

# In[4]:


# ----- Actors: 

def upload_actors_from_csv(csv_file: str):
    """
    Retrieve details (fullname, birthdate and imdb_id) about an actor from a CSV file.
    The CSV file is assumed to have columns: 
    imdb_id, name, birth_year

    Args:
        csv_file (str): Path to csv_file 
    Returns:
        actors (list): A list of Actors
    """
    ids, names, birth = extract_infos(csv_file=csv_file)
    actors = []
    for id, name, birth in zip(ids, names, birth):
        with open(f"data/celebrities_in_json/{name}.json", "r", encoding="utf-8") as file:
            # load file
            json_file = json.load(file) 
            # Extract bio
            actor_bio = json_file["data"]["name"]["bio"]["text"]["plainText"]
            actor_dic = ActorCreate(
                imdb_id=id,
                name=name,
                birthday=birth,
                biography=actor_bio
            )
            actors.append(actor_dic)
    return actors


# ----- Awards: 

def upload_awards_from_csv(csv_file: str, db: Session):
    """_This function uploads the data of all `award` info of and actor and stores them in a database
    It is a helper function, which will be called in the fastapi endpoint
    Args:
        csv_file (str): CSV file
        db (Session): Database Session used for communication 
    Raises:
        HTTPException: Exception if the Actor cannot be found
    Returns:
        award_create_list (list): A list of Awards 

    """
    if not os.path.exists(csv_file) or not db:
        print(f"File or Session does not exist or could not be created!!")
        return None
    ids, names, birth = extract_infos(csv_file=csv_file)
    award_create_list = []  # list to collect AwardCreate instances
    for id, name, birth in zip(ids, names, birth):
        actor_filename = f"data/celebrities_in_json/awards/Award_{name}.json"
        with open(actor_filename, "r", encoding="utf-8") as file:
            jf = json.load(file)
            award_data = award_data = jf.get("data", {}).get("name", {}).get("awardNominations", {})
            #jf["data"]["name"]["awardNominations"]
            actor_id = jf["data"]["name"]["id"]
            awardNominations = award_data["total"]
            actor_instance = db.query(Actor).filter(Actor.imdb_id == actor_id).first()
            if actor_instance is None:
                raise HTTPException(status_code=404, detail=f"Actor {name} with ID {actor_id} not found")
            # Collect raw award details from JSON.
            raw_awards = []
            for node in award_data["edges"]:
                if node["node"]["isWinner"] == True:
                    raw_awards.append({
                        "award_name": node["node"]["award"]["awardName"],
                        "year": node["node"]["award"]["eventEdition"]["year"]                   
                    })
            if raw_awards:
                years = [award["year"] for award in raw_awards]
                award_names = [award["award_name"] for award in raw_awards]
            else:
                years = []
                award_names = []
            # Create an AwardCreate instance using the extracted data.
            # Using the pydantic Class as it helps verifiy the data inputs before putting it in the database 
            db_award = AwardCreate(
                actor_id=actor_instance.id,
                actor_name=name,
                nominations=awardNominations,
                year=years,
                award_name=award_names,
                award_won=len(raw_awards)
            )
            award_create_list.append(db_award)
    return award_create_list


# ----- Movies: 
def upload_movies_from_csv(csv_file:str, db: Session):
    """
    This function uploads the movies of all actors in the database

    Args: 
        csv_file (str): CSV file 
        db (Session): A session of the database used to store the info in the database
    Returns:
        movie_create_list (str): A list of Movies 
    """
    ids, names, _ = extract_infos(csv_file=csv_file)
    genre =  "not available"
    movie_create_list = []
    for id, name in zip(ids, names):        
        movie_file = f"data/celebrities_in_json/movies/Movie_{name}.json"
        movie_file = movie_file.replace("..", ".")
        with open(movie_file, "r", encoding="utf-8") as movefile:
            jf = json.load(movefile)
            known_for = jf.get("data", {}).get("name", {}).get("knownFor", {})
        for node in known_for["edges"]:
            movie_id = node["node"]["title"]["id"]
            title = node["node"]["title"]["titleText"]["text"]
            year = node["node"]["title"]["releaseYear"]["year"]
            rating = node["node"]["title"]["ratingsSummary"]["aggregateRating"]
            # get actor id relationship
            actor_instance = db.query(Actor).filter(Actor.imdb_id == id).first()
            if actor_instance == None:
                raise HTTPException(status_code=500, detail=f"Actor {name} with ID {id} not found")
            db_movie = MovieCreate(
                actor_id=actor_instance.id,
                actor_name=name,
                movie_id=movie_id, 
                title=title,
                year= year, 
                rating=rating,
                genre=genre
            )
            movie_create_list.append(db_movie)
    return movie_create_list


# ## ------------ PUT  Functions

# In[5]:


def modify_movie_genre(movie_id: str, genre: str, db: Session):
    """This function updates the genre of a specific movie
    Args:
        movie_id (str): Movie ID 
        db (Session): A database session 
        genre (str): Genre
    Returns:
        updated_movie (list): Movie that was updated
    """
    movie = db.query(Movie).filter(Movie.movie_id == movie_id).first() 
    updated_movie = []
    if movie:
        movie.genre = genre 
        db.commit()
        db.refresh(Movie)
    else:
        raise HTTPException(status_code=500, detail=f"Movie with ID {movie_id} could not be found!")
    return updated_movie.append(
        Movie.title, 
        Movie.id, 
        Movie.genre
    )


# ## ------- FastAPI: Root function 

# In[6]:


@fastapi_app.get("/")
def root_api():
    return {"message: Star list discover the 50 top celebreities"}


# ### ------------FastAPI: POST ~  Uploading Data to the Database -----------

# In[7]:


# ---------------------- Uploading Data to the Database from csv and json file -----------------------------

@fastapi_app.post("/upload_actors/", response_model=List[ActorCreateResponse])
async def upload_actors(db: Session = Depends(get_db)):
    """This is a fastapi endpoint that posts all actor data in the database

    Args:
        db (Session): Database session 
        ActorCreationResponse (list): Validated response by the pydantic BaseModel
    Return:
        created_actors (list): A list of all actors created or an exception error when something went wrong"""

    try:
        actor_list = upload_actors_from_csv(csv_file=csv_file)
        created_actors = []
        for actor in actor_list: 
            db_actor = Actor(
                name=actor.name,
                imdb_id=actor.imdb_id,
                birthday = actor.birthday,
                biography = actor.biography           
            )
            db.add(db_actor)
            db.commit()
            db.refresh(db_actor)
            created_actors.append(db_actor)
        return created_actors
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")

@fastapi_app.post("/upload_awards/", response_model=List[AwardCreateResponse])
async def upload_awards(db: Session = Depends(get_db)):
    """This function is a fastapi endpoint that uploads the award of all actors in the database

    Paramters:
        db (session): Database Session 
        AwardCreateResponse (list): Pydantic BaseModel that handles Award uploads
    Raises:
        HTTPException: Raises an exception when there is an internal error

    Returns:
        created_awards (list): List of all awards created"""

    try:
        awards_list = upload_awards_from_csv(csv_file=csv_file, db=db)
        created_awards = []
        for award in awards_list:
            db_award = Award(
                actor_id=award.actor_id, 
                actor_name=award.actor_name,
                award_name=award.award_name, 
                year=award.year,  
                nominations=award.nominations, 
                award_won=award.award_won
            )
            db.add(db_award)
            db.commit()
            db.refresh(db_award)
            created_awards.append(db_award)
        return created_awards
    except Exception as e: 
        raise HTTPException(status_code=500, detail=f"Error: {e}")

@fastapi_app.post("/upload_movies/", response_model=List[MovieResponse])
async def upload_movies(db: Session = Depends(get_db)):
    """This fastapi endpoint uploads the movies into the database

    Args:
        db (database): Database session 
    Returns:
        created_movies (obj): List of Movie Response Objects for movies for actors"""
    try:
        movies = upload_movies_from_csv(csv_file=csv_file, db=db)
        created_movies = []
        for movie in movies:
            db_movie = Movie(
                actor_id=movie.actor_id,
                actor_name=movie.actor_name,
                movie_id=movie.movie_id,
                title=movie.title,
                year=movie.year,
                genre=movie.genre,
                rating=movie.rating
            )
            db.add(db_movie)
            db.commit()
            db.refresh(db_movie)
            created_movies.append(db_movie)
        return created_movies
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Error: {err}")


# ### ---- FastApi: ~ GET: For retrieving data from the database  ---

# In[8]:


@fastapi_app.get("/actor/{actor_id}", response_model=ActorCreateResponse)
async def read_actor(actor_id: int, db: Session = Depends(get_db)):
    """This funtion retrieves a specific Actor's infos from the database

    Parameter:
        actor_id (int): Unique ID of an actor

    Returns:
        db_actor_item (json): The information of an actor in json schema"""

    db_actor_item = db.query(Actor).filter(Actor.id == actor_id).first()
    if db_actor_item is None:
        raise HTTPException(status_code=404, detail="Actor not found")
    return db_actor_item


@fastapi_app.get("/award/{actor_id}", response_model=AwardCreateResponse)
async def read_award(actor_id: int, db: Session = Depends(get_db) ):
    """This particular code snippet defines a GET endpoint in a FastAPI application."""
    db_award_item = db.query(Award).filter(Award.actor_id == actor_id).first()
    if db_award_item is None:
        raise HTTPException(status_code=500, detail="Actor not Found, Award could not be found either")
    return db_award_item


@fastapi_app.get("/movie/{actor_id}", response_model=List[MovieResponse])
async def read_movie(actor_id: int, db: Session = Depends(get_db)):

    """This endpoint is a GET request handler in a FastAPI application. 
    It is designed to retrieve a list of movies associated with a specific actor 
    based on the `actor_id` provided in the URL path parameter."""

    db_movie_items = db.query(Movie).filter(Movie.actor_id == actor_id).all()
    if db_movie_items is None:
        raise HTTPException(status_code=404, detail=f"Actor not Found")
    return db_movie_items


@fastapi_app.get("/most_popular_celebrities", response_model=List[ActorCreateResponse])
async def most_popular_actors(db: Session = Depends(get_db)):
    """This function returns the most popular Celebrities"""
    return db.query(Actor).all()


@fastapi_app.get("/movies", response_model=List[MovieResponse])
async def most_popular_movies(db: Session = Depends(get_db)):
    """This function displays movies of most popular actors"""
    return db.query(Movie).all()

@fastapi_app.get("/actors/{actor_id}", response_model=ActorMovieResponse)
async def top_five_actor_movies(actor_id: int, db: Session = Depends(get_db)):
    """This function get the top 5 movies of an actor"""
    db_actor = db.query(Actor).options(joinedload(Actor.movies)).filter(Actor.id == actor_id).first()
    if db_actor is None: 
        raise HTTPException(status_code=404, detail=f"Actor with the ID: {actor_id} could not be found")

    return ActorMovieResponse(
        id=db_actor.id,
        name=db_actor.name,
        birthday=db_actor.birthday,
        biography=db_actor.biography,
        movies=[MovieResponse(
            id = movie.id,
            movie_id = movie.movie_id,
            actor_id=movie.actor_id,
            actor_name=movie.actor_name,
            title=movie.title,
            year=movie.year,
            genre=movie.genre,
            rating=movie.rating

        ) for movie in db_actor.movies[:5]]

    )  


# ### ---- ~ FastApi: Update Database 

# In[9]:


@fastapi_app.put("/update_movie/{movie_id}", response_model=UpdateGenre)
async def update_movie_genre(movie_id: str, genre: str, db: Session  = Depends(get_db)):
    """This function updates the genre of a movie using fastapi endpoint
    Arg:
        movie_id (str): Movie ID 
        genre (str): Movie Genre 
        db (session): Database Session 
    Returns:
        db_movie_update (db_query): Updated version of the movie entry

    """
    db_movie_update = modify_movie_genre(movie_id=movie_id, genre=genre, db=db)
    return db.query(Movie).filter(Movie.movie_id == movie_id).first()


# ## ------- Run FastAPI ----

# In[ ]:


# # To avoid conflict in Jupyter Notebook when using Fastapi
# def connect():
#     import nest_asyncio
#     import uvicorn
#     nest_asyncio.apply()
#     uvicorn.run(fastapi_app, port=8000)

