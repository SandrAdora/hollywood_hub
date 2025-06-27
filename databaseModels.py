

import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, Float
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from pydantic import BaseModel
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine

# --------------------------------------------------------------------- Database Setup ----------------------------------------------------------------------------



engine = create_engine("sqlite:///celeb.db")
SessionLocal = sessionmaker(expire_on_commit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ---------------------------------------------------------------------- SQLAlchemy Models -------------------------------------------------------------------------

class Actor(Base):
    __tablename__ = "actors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    imdb_id = Column(String)
    name = Column(String, nullable=False)
    birthday = Column(String)
    biography = Column(String)
    movies = relationship("Movie", back_populates="actor")
    awards = relationship("Award", back_populates="actor")

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    actor_id = Column(Integer, ForeignKey("actors.id"))
    actor_name = Column(String)
    movie_id = Column(String)
    title = Column(String)
    year = Column(Integer)
    genre = Column(String, nullable=True)
    rating = Column(Float, nullable=True)
    actor = relationship("Actor", back_populates="movies")
    

class Award(Base):
    __tablename__ = "awards"

    id = Column(Integer, primary_key=True, autoincrement=True)
    actor_id = Column(Integer, ForeignKey("actors.id"))
    actor_name = Column(String)
    award_name = Column(JSON, nullable=False)
    nominations = Column(Integer, nullable=True) 
    year = Column(JSON, nullable=True) 
    award_won = Column(Integer, nullable=True)
    # Creating relationship to actor class
    actor = relationship("Actor", back_populates="awards")


# ------------- Create Tables ----------
Base.metadata.create_all(engine)

# --------------------------------------------------------------- End of SQLAlchemy Database ----------------------------------------------------------------------
# import sqlite3

# class HollywoodDatabase:
#     def __init__(self, db_name="hollywood.db"):
#         """
#         The code defines a Python class that connects to an SQLite database, creates tables for actors,
#         movies, and awards, inserts data into these tables, fetches actor details, and closes the database
#         connection.
        
#         :param db_name: The `db_name` parameter in the `__init__` method of the class is a default parameter
#         that specifies the name of the SQLite database file to connect to. If no database name is provided
#         when creating an instance of the class, it will default to "hollywood.db", defaults to hollywood.db
#         (optional)
#         """
#         """Initialize connection to SQLite Database"""
#         self.conn = sqlite3.connect(db_name)
#         self.cursor = self.conn.cursor()
#         self.create_tables()

#     def create_tables(self):
#         """Create database tables if they do not exist"""
#         self.cursor.execute("""
#             CREATE TABLE IF NOT EXISTS actors (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 imdb_id TEXT,
#                 name TEXT UNIQUE, 
#                 birth_date TEXT
#                 biography TEXT
#             );
#         """)

#         self.cursor.execute("""
#             CREATE TABLE IF NOT EXISTS movies (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 actor_id INTEGER,    
#                 title TEXT, 
#                 year INTEGER, 
#                 genre TEXT, 
#                 rating REAL, 

#                 FOREIGN KEY(actor_id) REFERENCES actors(id)
#             );
#         """)

#         self.cursor.execute("""
#             CREATE TABLE IF NOT EXISTS awards (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 award_nominations INTEGER,
#                 award_name TEXT,
#                 year INTEGER,
#                 award_won INTEGER,
#                 actor_id INTEGER,
#                 FOREIGN KEY(actor_id) REFERENCES actors(id)
#             );
#         """)

#         self.conn.commit()

#     def insert_actor(self, name, biography, birth_year):
#         """Insert actor into the database"""
#         try:
#             self.cursor.execute("INSERT INTO actors (name, biography, birth_year) VALUES (?, ?, ?)",
#                                 (name, biography, birth_year))
#             self.conn.commit()
#             return f"Actor {name} added successfully."
#         except sqlite3.IntegrityError:
#             return f"Actor {name} already exists."

#     def insert_movie(self, title, year, genre, rating, actor_id):
#         """Insert movie into the database"""
#         self.cursor.execute("INSERT INTO movies (title, year, genre, rating, actor_id) VALUES (?, ?, ?, ?, ?)",
#                             (title, year, genre, rating, actor_id))
#         self.conn.commit()
#         return f"Movie {title} added successfully."

#     def insert_award(self, award_name, year, award_won, actor_id):
#         """Insert award into the database"""
#         self.cursor.execute("INSERT INTO awards (award_nominations, award_name, year, award_won, actor_id) VALUES (?, ?, ?, ?,?)",
#                             (award_name, year, award_won, actor_id))
#         self.conn.commit()
#         return f"Award {award_name} added successfully."

#     def get_actor(self, name):
#         """Fetch actor details from database"""
#         self.cursor.execute("SELECT * FROM actors WHERE name=?", (name,))
#         actor = self.cursor.fetchone()
#         return actor if actor else f"Actor {name} not found."

#     def close_connection(self):
#         """Close database connection"""
#         self.conn.close()

