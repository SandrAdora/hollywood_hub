from typing import List, Optional
from pydantic import BaseModel

# -----------------------------------------------------Pydantic Models for Validation and Response -------------------------------------------------------------------

class ActorCreate(BaseModel):
    
    imdb_id : str | None
    name: str
    birthday: str
    biography: str
    

class ActorCreateResponse(BaseModel):
    id: int
    imdb_id:  str | None
    name: str 
    birthday: str
    biography: str
    
    #helps translate  database table records to a class object
    class Config: 
        from_attributes  = True

class AwardCreate(BaseModel):
    
    actor_id: Optional[int]
    actor_name: str
    nominations: Optional[int] 
    award_name: List[str] | None
    year: List[int] | None
    award_won: int | None

    
class AwardCreateResponse(BaseModel):
    id: int 
    actor_id: Optional[int]
    actor_name: str
    nominations: int | None
    award_name: List[str] | None
    year: List[int] | None
    award_won: int
    
    class Config:
        from_attributes  = True

class MovieCreate(BaseModel):
    
    actor_id : Optional[int]
    actor_name: str
    movie_id: str
    title:  str
    year : int
    genre : Optional[str]
    rating : Optional[float]

class MovieResponse(BaseModel):
    
    id: int
    actor_id: Optional[int]
    actor_name: str
    movie_id: str
    title: str
    year: int
    genre: Optional[str]
    rating: Optional[float]
    
    class Config: 
        from_attributes  = True

class ActorMovieResponse(BaseModel):
    
    id: Optional[int]
    name: str
    birthday: str
    biography: str 
    movies: List[MovieResponse]

class UpdateGenre(BaseModel):
    id: int
    genre: str
    title:str

class UpdateGenreResponse(BaseModel):
    id: int
    title: str
    genre: str