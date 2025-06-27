import json 
import http.client 
import csv
import requests
import os
import shutil
import re

from PIL import Image
from fastapi import HTTPException


# ------- Fast API URL ----------------
# Only visable when server is running
FASTAPI_URL_SWAGGER = "http://127.0.0.1:8000/docs" # Shows all Endpoints at once [strg + click]
FASTAPI_URL = "http://127.0.0.1:8000/" # root
FASTAPI_CELEBS_URL = "http://127.0.0.1:8000/most_popular_celebrities"
FASTAPI_MOVIES = "http://127.0.0.1:8000/movies"

"http://127.0.0.1:8000/actors/1" # <----- you can try out different numbers [1 - 50]
"http://127.0.0.1:8000/actor/1" # <----- you can try out different numbers [1 - 50]
"http://127.0.0.1:8000/award/1" # <----- you can try out different numbers [1 - 50]
"http://127.0.0.1:8000/movie/3" # <----- you can try out different numbers [1 - 50]



API_Key = "9fa984d914msh403466552cf5607p188a09jsnaf88eb2f8b19"                                                      
IMDb = "imdb-com.p.rapidapi.com"#"imdb232.p.rapidapi.com"#"imdb8.p.rapidapi.com"  


# ------- CSV Infos about Celebs
def csv_path():
    return "data/actors_ids_names_birthdates.csv"

def extract_infos(csv_file):
    """This function loads a csv file to extract the ids, names and birthdays of the most popular actors and then stores them in lists

    Args:
        csv_file (csv): Contains the list of the 50 most popular celebrities
    Returns:
        List: A tupel of lists Actor's IDs, Name and birthdate
        
    """ 
    if not os.path.exists(csv_file):
        raise ValueError(f"File {csv_file} is empty!!")
    lines = []
    ids = []
    names =[]
    birthdates = []
    i = 1
    if not os.path.exists(csv_file):
        raise ValueError(f"File path {csv_file} does not exit!!!")
    with open( csv_file, mode="r") as file:
        csvfile = csv.reader(file)
        
        # find the number of columns
        headers = len(next(csvfile))
                
        for line in csvfile:
            lines.append(line)
    if headers <= 3:
        for i in range(len(lines)):
            ids.append(lines[i][0])
            names.append(lines[i][1])
            birthdates.append(lines[i][2])
    elif headers > 3:
        # Extract idis from file 
        for i in range(len(lines)):
            ids.append(lines[i][1])
            names.append(lines[i][5])
            birthdates.append(lines[i][7])
    return ids, names, birthdates



def create_actor_csv(csv_file):
    """
    Extracts actor data and writes it to a CSV file.  
    Args:
        csv_file (str): Path to the CSV file containing actor information.
    Returns:
        str: A success message indicating the file creation.
    """
    # Extract data from the CSV
    ids, names, birthdates = extract_infos(csv_file=csv_path())

    # Prepare structured data (list of lists)
    actor_data = list(zip(ids, names, birthdates))  # Converts to proper row format
    if actor_data:

        # Write data to CSV file
        with open("actors_ids_names_birthdates.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["IMDb ID", "Name", "Birthdate"])  # Header row
            writer.writerows(actor_data)  # Write each actor row
    else:
        raise ValueError(f"Could not create a list Following reasons could be ID:{id}, Names:{names} or Birthdates: {birthdates} are empty!!")

    return "Created File successfully"








def http_request_api(api_key, imdb_host):
    """Establishes a HTTPS connection with IMDb using the provided API Key and host.
    
    Args:
        api_key (str): API Key.
        imdb_host (str): IMDb domain (Rapid API).
    
    Returns:
        tuple: HTTPS connection and headers dictionary.
    """
    try:
        conn = http.client.HTTPSConnection(imdb_host)
        headers = {'x-rapidapi-key': api_key, 'x-rapidapi-host': imdb_host}
        return conn, headers
    except Exception as err:
        return f"Error: {err}!"






def infos(f, api, imdb, ty_ ):
    """This function generates a jsonfiles for each actor
    
    Args:
        f (str): CSV file
        api (str): API Key
        imdb (str): Domain (Rapid API ) 
    Returns:
        str: Notificatin File was created
    """
    _, names, _ = extract_infos(csv_file=f)
    for name in names:    
        conn, headers = http_request_api(API_Key=api, IMDb=imdb)
        if ty_ == "bio":
            endpoint = f"/api/actors/get-bio?={name}"
        elif ty_ == "award":
            endpoint = f"/api/actors/get-awards?nm={name}"
            
        if conn.request("GET", endpoint, headers=headers):
            res = conn.getresponse()
            data = res.read()
            jaf = json.loads(data.decode("utf-8"))
            for name in names:
                with open(f"celebrities_in_json/{name}.json", "w", encoding="utf-8") as file:
                    json.dump(jaf, file, indent=4,  ensure_ascii=False)
        else:
            raise HTTPException(status_code=500, detail={f"Connection could not be granted"})
    return f"Actor Best Known for {name} was created"




def get_actors_best_known_for_movies(f, api, imdb):
    """Retrieve an actor's best-known movies and write them to separate JSON files.
    Args:
        f (str): CSV file 
        api (str): API Key 
        imdb (str): Domain (Rapid API)
    Returns:
        str (str): Notification that file was created
    """
    
    ids, names, _ = extract_infos(csv_file=f)

    for id, name in zip(ids, names):    
        conn, headers = http_request_api(API_Key=api, IMDb=imdb)
        print(f"Fetching data for: {name} (ID: {id})")
        
        endpoint = f"/actor/get-know-for?nconst={id}"
        conn.request("GET", endpoint, headers=headers)
        res = conn.getresponse()
        data = res.read()

        try:
            jaf = json.loads(data.decode("utf-8"))
        except json.JSONDecodeError:
            print(f"Error decoding JSON for actor {name}")
            continue

        file_path = f"data/celebrities_in_json/movies/Movie_{name}.json"
        with open(file_path, "w", encoding="utf-8") as mov:
            json.dump(jaf, mov, indent=4, ensure_ascii=False)

        print(f"Created file for {name}: {file_path}")

    return "Actor best-known movie data files created."







def img_url_extractor(actor_id: str, actor_name: str, choice="actor"):
    """Returns the URL of an actor or a list of URLs of movies the actor starred in.
    Args:
        actor_id (str): Actor ID as IMDb str
        actor_name (str): Actor's name
        choice (str): What file to extract URL from (actor or movie)
    Returns:
        url (str): URL or List of URLs or None if no url was located 
    """   
    
    if choice == "actor":
        with open(f"data/celebrities_in_json/{actor_name}.json", "r", encoding="utf-8") as j_file:
            data = json.load(j_file)
            child = data["data"]["name"]
            if child["id"] == actor_id:
                return child.get("primaryImage", {}).get("url", None)
            else:
                print(f"Actor not found: {actor_name}")
                return None
    elif choice == "movie":
        list_of_movies = [] 
        with open(f"data/celebrities_in_json/movies/Movie_{actor_name}.json", "r", encoding="utf-8") as j_movie:
            data = json.load(j_movie)
            url_path = data["data"]["name"]["knownFor"]["edges"]
            for child in url_path:
                title_info = child["node"].get("title", {})
                list_of_movies.append({
                    "title": title_info.get("titleText", {}).get("text", "Unknown"),
                    "url": title_info.get("primaryImage", {}).get("url", None)
                })
        return list_of_movies          

    return None




def load_images(directory):
    """Loads all images from a given folder and returns them as a list of Image objects.

    Args:
        directory (str): Images folder 
        
    Returns:
        img_list (list): A list of imges
    """
    image_list = []    
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)       
        if file_name.lower().endswith(("jpg", "jpeg", "png", "bmp")):  # Check valid image formats
            img = Image.open(file_path)
            image_list.append(img)  
    return image_list



def load_image(img_path: str):
    """Loads and resizes a specified image file by (200 x 200).
    
    Args:
        img_path (str): Path to image as a string
    Returns:
        img (Image): Resized version of the image or None when image was not located
        """ 
    if not os.path.exists(img_path):  
        print(f"Error: File '{img_path}' not found.")
        return None
    try:
        img = Image.open(img_path)  
        resized_img = img.resize((200, 200), Image.Resampling.LANCZOS)  
        return resized_img  
    except IOError:
        print(f"Error loading image: '{img_path}'")
        return None




def save_image(actor_name: str, actor_id: str, choice="actor"):
    """Saves images of an actor in the image folder. It Calls `img_url_extractor()` to retrieve the URL of an actor's Image or movie image,
    downloads the URL as an image, and saves it in the image file.
    
    Args:
        actor_name (str): Name of an Actor
        actor_id (str): IMDb_ID of an Actor
    Returns:
        file_path (str): Path where the image is saved, or None if saving was not possible.
    """

    directory = "data/images"
    movie_destination = os.path.join(directory, f"movie_images_{actor_name.lower().replace(' ', '_')}")

    # Ensure both directories exist
    if not os.path.exists(directory):
        os.makedirs(directory)
    if not os.path.exists(movie_destination):
        os.makedirs(movie_destination)

    actor_name = actor_name.replace("..", ".")
    file_name = f"{actor_name.lower().replace(' ', '_')}.jpg"
    file_path = os.path.join(directory, file_name)

    URL = img_url_extractor(actor_id=actor_id, actor_name=actor_name, choice=choice)

    if choice == "movie":    
        if not URL or not isinstance(URL, list):  # Ensure URL is valid
            print(f"Error: No valid movie images found for {actor_name}")
            return None

        for item in URL:
            if isinstance(item, dict) and 'url' in item:
                res = requests.get(item['url'], stream=True)
                title = item["title"].lower().replace(" ", "_")
                #.replace("/", "_").replace("?", "_").replace("!", "_").replace("..", "_").replace(":", "_")
                title = re.sub(r'[\/:*?"<>|]', '_', title)
                movie_path = os.path.join(movie_destination, title + ".jpg")
                with open(movie_path, "wb") as movie_output: 
                    shutil.copyfileobj(res.raw, movie_output)
                print(f"Saved {actor_name}'s movie to {movie_path}")
        return movie_destination

    elif choice == "actor":
        if not URL:
            print(f"Error: No image URL found for {actor_name}")
            return None
        
        # Download as a picture 
        res = requests.get(URL, stream=True)
        with open(file_path, "wb") as output:
            shutil.copyfileobj(res.raw, output)
        print(f"Saved {actor_name}'s image to {file_path}")
        return file_path

    return None




def available_actors(pos: int, file=csv_path()):
    """ This is a help function that list out the name and imdb id of a specific actor
    and returns them as seperate values
    
    Args:
        pos (int): Position to search for 
        
    Returns:
        key (str): A Key --> Actor's ID
        value (str): A value --> Actor's Name
    """   
    ids, names, _ = extract_infos(csv_file=file)
    # create a dictionary 
    actors_dic = {name: id for name, id in zip(names, ids)}
    key = list(actors_dic.keys())[pos]
    value = actors_dic[key]
    return key, value

def average_rating_of_each_actor(actor: str):
    """This function calculates the anual avarage rating of each actor
    based on the rating of movies they stared in. It extracts the ratings of each movie 
    from the list of movies and calculates the arithemic average
    
    Args:
        actor (list): name of an actor 
    Returns:
        average_rating (float): The average rating of each actor based on movies 
"""
    average_rating = .0
    list_of_ratings = []
    res = requests.get(FASTAPI_MOVIES)
    if res.status_code != 200:
        print(f"Error: No connection possible: {res.status_code}")
        return None 

    celebs = res.json() 
    for celeb in celebs: 
        if celeb["actor_name"].lower() == actor.lower():
        
            list_of_ratings.append(
                celeb["rating"]
            )
    
    if len(list_of_ratings) > 0:
        average_rating = sum(list_of_ratings) / len(list_of_ratings)
        return average_rating
    return None

def best_known_for_genre(name: str):
    """This is a helper function that returns the genre of an actor based on films he/she is normaly stared in 
        Args:
            name: Name of an Actor
        Returns:
            known_for_genre (str): What the Actor normaly stars in or None when actor could not be found
        
    """
    name = name.lower()
    genres_by_actor = {
        "johnny depp": "fantasy/comedy",
        "al pacino": "crime/thriller",
        "robert de niro": "crime/drama",
        "kevin spacey": "drama/thriller",
        "denzel washington": "action/thriller",
        "russell crowe": "historical drama/action",
        "brad pitt": "drama/action",
        "angelina jolie": "action/fantasy",
        "leonardo dicaprio": "biographical drama",
        "tom cruise": "action",
        "john travolta": "action/drama",
        "arnold schwarzenegger": "action/sci-fi",
        "sylvester stallone": "action",
        "kate winslet": "romantic drama",
        "christian bale": "psychological thriller/action",
        "morgan freeman": "drama/thriller",
        "keanu reeves": "action/sci-fi",
        "nicolas cage": "action/thriller",
        "hugh jackman": "superhero/action",
        "edward norton": "psychological thriller/drama",
        "bruce willis": "action",
        "tom hanks": "drama/comedy",
        "charlize theron": "action/sci-fi",
        "will smith": "action/sci-fi",
        "sean connery": "spy/action",
        "keira knightley": "historical drama",
        "vin diesel": "action",
        "matt damon": "action/thriller",
        "richard gere": "romantic drama",
        "catherine zeta-jones": "musical/action",
        "clive owen": "action/thriller",
        "mel gibson": "historical action",
        "george clooney": "drama/comedy",
        "jack nicholson": "psychological drama",
        "scarlett johansson": "action",
        "tom hardy": "action/thriller",
        "robert downey jr.": "superhero/comedy",
        "orlando bloom": "fantasy/action",
        "ian mckellen": "fantasy",
        "antonio banderas": "action/musical",
        "guy pearce": "drama/thriller",
        "samuel l. jackson": "action/thriller",
        "sandra bullock": "romantic / comedy",
        "meg ryan": "romantic comedy",
        "megan fox": "action",
        "nicole kidman": "drama/thriller",
        "gerard butler": "action",
        "simon baker": "drama",
        "cameron diaz": "drama",
        "katherine heigl": "romantic /comedy"
        }
    for actor, genre in genres_by_actor.items():
        if actor == name:
            return genre
    return None


# --------------------------------------------------------------------------------------------------- Depreciated --------------------------------------------------------------------------------------
# def img_to_array(img):
#     """Converts an image to a Numpy array"""
#     img = Image.open(img)
#     img_array = np.array(img)
#     return img_array

# def searcher(position, csv_file):
#     """This helper function searches for the name and id of an actor at a specific position
#     Parameters:
#         position (int): Position of an Actor
#         csv_file (str): CSV file
#     Returns:
#         tupel: (Actor name, Actor's ID)
#     """
#     if position <= 0:
#         print("No actor at this position ")
#         return None, None
#     ids, names, _ = extract_infos(csv_file=csv_file)
#     # create a dictionary 
#     actors_dic = {name: id for name, id in zip(names, ids)}
#     if position >= len(actors_dic):
#         print("Postion is not in the valid scope")
#         return None, None
#     return list(actors_dic.items())[position]


# def img_translator(actor_id: str, actor_name: str):
#     """Fetches the image of an actor using their IMDb ID. 
#     Parameters:
#         actor_id (str): Actor IMDb ID
#         actor_name (str): Actor Name       
#     Returns:
#         tuple: (Actor name, Image object) or (Actor name, None) if image not found
#     """
#     img_url = img_url_extractor(actor_id=actor_id, actor_name=actor_name)

#     if not img_url:  # Ensure img_url isn't None
#         print(f"Error: No image URL found for {actor_name}.")
#         return actor_name, None
#     try:
#         res = requests.get(img_url)
#         res.raise_for_status()  # Raise error for failed requests
#         img = Image.open(BytesIO(res.content))  # Convert to Image object
#         resized_img = img.resize((200, 200))  # Resize
#         return actor_name, resized_img  # Return tuple  
#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching image for '{actor_name}': {e}")
#         return actor_name, None   
#     except UnidentifiedImageError:
#         print(f"Error: Invalid image format for '{actor_name}'.")
#         return actor_name, None

# def extract_celeb_infos(API_key=API_Key, IMDb=IMDb, actor_id ="nm5097044", what_infos="bio"): 
#     """ The extract_celeb_infos() function retrieves information about a Hollywood actor or actress using their IMDb ID. 
#     It queries various types of data such as biography, awards, and movie history using the get_actor_infos() 
#     function and processes the JSON response into a structured format Args: actor_id (str): IMDb ID"nm5097044
#     what_infos (str, optional): Specifies which information to retrieve ("bio", "award", "movie"). Default is "bio".. 
#     Defaults to "bio". Returns: List: If what_infos == "bio" → Returns a tuple with: Actor ID Actor Name Actor Biography I
#     f what_infos == "award" → Returns a list of tuples, each containing: Total award nominations Award name Year Category Actor ID 
#     If what_infos == "movie" → Returns a list of tuples, each containing: Actor’s Name """ 
#     try: 
#         if what_infos == "bio": 
#             json_data = get_actor_biography(API_Key=API_Key, IMDb=IMDb, imdb_id=actor_id) 
#             data = json.loads(json_data) 
#             name_data = data["data"]["name"] 
#             # Extracts name information 
#             actor_bio = { 
#                 "id": name_data["id"], 
#                 "name": name_data["nameText"]["text"], 
#                 "image_url": name_data["primaryImage"]["url"],
#                 "biography": name_data["bio"]["text"]["plainText"] 
#                 } 
#             return actor_bio["id"], actor_bio["name"], actor_bio["biography"] 
#         elif what_infos == "award": 
#             award_json = get_actor_awards(API_Key=API_Key, IMDb=IMDb, imdb_id=actor_id) 
#             data_award = json.loads(award_json) 
#             award_data = data_award["awardNominations"] 
#             actor_awards = [
#                 (
#                     award_data["total"],  # Handle missing 'total'
#                     node["node"]["award"]["awardName"],  # Award name
#                     node["node"]["award"]["eventEdition"]["year"],  # Year
#                     node["node"]["category"]["text"],  # Category
#                     award_data["id"]  # Actor ID
#                 )
#                 for node in award_data["edges"]  # Avoid errors if 'edges' is missing
#                 if node["node"]["isWinner"]  # Ensure 'isWinner' exists
#             ]

#             return actor_awards 
#         elif what_infos == "movie": 
#             json_data = get_movies(API_Key=API_Key, IMDB=IMDb, imdb_id=actor_id) 
#             meta = json.loads(json_data) 
#             movie_data = meta["data"]["names"][0]["knownFor"]["edges"] # First actor's known movies 
#             actor_movies = [
#                 (
#                     movie["node"]["title"]["titleText"]["text"],  # Movie Title
#                     movie["node"]["title"]["releaseYear"]["year"] if "releaseYear" in movie["node"]["title"] else "Unknown Year",  # Release Year
#                     movie["node"]["title"]["ratingsSummary"]["aggregateRating"] if "ratingsSummary" in movie["node"]["title"] else "No Rating"  # Ratings
#                 )
#                 for movie in movie_data
#                 if movie["node"]["title"]["titleType"]["categories"][0]["id"] == "movie"  # Check if it's a movie
#             ]

#             actor_movies_sorted = sorted(actor_movies, key=lambda x: x[2], reverse=True) 
#             return actor_movies_sorted 
#     except KeyError as e: 
#         return {"error": f"Missing key in JSON: {str(e)}"} 
#     except json.JSONDecodeError: 
#         return {"error": "Invalid JSON response format."} 
#     ##################################################################################################################### 
#     def get_list_of_most_popular_celeb(API_Key, IMDb):
#         conn, headers = http_request_api(API_Key=API_Key, IMDb=IMDb) 
#         conn.request("GET", "/actors/list-most-popular-celebs?homeCountry=US&currentCountry=US&purchaseCountry=US", headers=headers) 
#         res = conn.getresponse() 
#         data = res.read() 
#         actors = json.loads(data.decode("utf-8")) 
#         actor_ids = [actor.replace("/name/", "").strip("/") for actor in actors] 
#         return actor_ids
#     ##################################################################################################################### 
# def get_actor_biography(API_Key, IMDb, imdb_id): 
#     """This function retrieves the biography of an actor. :params: API_Key: for autentification IMDB: Domain from which the data is fetched imdb_id: Actor's ID :return: Actor's Biography """ 
#     conn, headers = http_request_api(API_Key=API_Key, IMDb=IMDb) 
#     conn.request("GET", f"/actors/v2/get-bio?nconst={imdb_id}&country=US&language=en-US", headers=headers) 
#     res = conn.getresponse() 
#     data = res.read() 
#     actors = json.loads(data.decode("utf-8")) 
#     return json.dumps(actors, indent=4, sort_keys=True) 
# ##################################################################################################################### 
# def get_actor_awards( API_Key, IMDb, imdb_id="nm5097044"): 
#     """This function retrieves the Awards of a specific actor. Args: API_Key (_type_): _description_ IMDb (_type_): _description_ imdb_id (str, optional): _description_. Defaults to "nm5097044". Returns: _type_: _description_ """ 
#     conn, headers = http_request_api(API_Key=API_Key, IMDb=IMDb) 
#     conn.request("GET", f"/actors/v2/get-awards?nconst={imdb_id}&country=US&language=en-US", headers=headers) 
#     res = conn.getresponse() 
#     data = res.read() 
#     actors = json.loads(data.decode("utf-8")) 
#     return json.dumps(actors, indent=4, sort_keys=True) 
# ##################################################################################################################### 


# def get_movies(API_Key, IMDB, imdb_id): 
#     """This functions retrieves the meta data of an actor. From the data it then extracts the movies and ratings of a specific actor Args: API (_type_): _description_ IMDB (_type_): _description_ imdb_id (_type_): _description_ Returns: _type_: _description_ """ 
#     conn, headers = http_request_api(API_Key=API_Key, IMDb=IMDB) 
#     conn.request("GET", f"/actors/v2/get-meta-data?nconsts={imdb_id}%2C{imdb_id}&first=20&country=US&language=en-US", headers=headers) 
#     res = conn.getresponse() 
#     data = res.read() 
#     actors = json.loads(data.decode("utf-8")) 
#     with open("actor_meta_data.json", "w", encoding="utf-8") as actor_meta_data: 
#         json.dump(actors, actor_meta_data, indent=4, ensure_ascii=False) 
#     return "Movies were loaded to a json file called actor_movies"
# def get_movies(API_Key, IMDB, imdb_id): 
#     """This functions retrieves the meta data of an actor. From the data it then extracts the movies and ratings of a specific actor Args: API (_type_): _description_ IMDB (_type_): _description_ imdb_id (_type_): _description_ Returns: _type_: _description_ """ 
#     conn, headers = http_request_api(API_Key=API_Key, IMDb=IMDB) 
#     conn.request("GET", f"/actors/v2/get-meta-data?nconsts={imdb_id}%2C{imdb_id}&first=20&country=US&language=en-US", headers=headers) 
#     res = conn.getresponse() 
#     data = res.read() 
#     actors = json.loads(data.decode("utf-8")) 
#     with open("actor_meta_data.json", "w", encoding="utf-8") as actor_meta_data: 
#         json.dump(actors, actor_meta_data, indent=4, ensure_ascii=False) 
#     return "Movies were loaded to a json file called actor_movies"
