# import json
# import http.client
# import os
# import csv
# import pandas as pd
# from helper_functions import extract_infos
# #####################################################################################################################     
# API_Key = "9fa984d914msh403466552cf5607p188a09jsnaf88eb2f8b19"
# IMDb = "imdb232.p.rapidapi.com"#"imdb8.p.rapidapi.com"

# #####################################################################################################################  

# class IMDB_Celeb:
#     """Class to interact with the IMDb API and retrieve actor-related data."""
#     # Contructor
#     def __init__(self, api_key, imdb_host):
#         self.api_key = api_key
#         self.imdb_host = imdb_host
#         self.conn = http.client.HTTPSConnection(self.imdb_host)
#         self.headers = {
#             'x-rapidapi-key': self.api_key,
#             'x-rapidapi-host': self.imdb_host
#         }

#     # Getter Methods
#     def _make_request(self, endpoint):
#         """
#         The `_make_request` function sends a GET request to a specified endpoint, reads the response, and
#         returns the JSON data decoded from UTF-8.
        
#         :param endpoint: The `endpoint` parameter in the `_make_request` method is a string that represents
#         the specific endpoint or URL to which the HTTP GET request will be made. This endpoint typically
#         corresponds to a specific resource or service that the client wants to interact with
#         :return: The function `_make_request` is returning the JSON data obtained from the response of a GET
#         request to the specified `endpoint`.
#         """
#         self.conn.request("GET", endpoint, headers=self.headers)
#         res = self.conn.getresponse()
#         if res.status != 200:
#             raise ValueError(f"Error recivied Status code {res.status}")
#         data = res.read()
        
#         return json.loads(data.decode("utf-8"))

#     def get_actor_biography(self, name):
#         """This function returns the biography of a given Actor

#         Args:
#             name (string): Actor's Name

#         Returns:
#             string: The complete biography of an actor
#         """
#         # Using endpoint is depreciated 
#         #endpoint = f"/api/actors/get-bio?nm={imdb_id}"
#         with open(name.json, "r", encoding="utf-8") as file:
#             jf = json.load(file)
#             return jf["data"]["name"]["bio"]["text"]["plainText"]
        
#         return self._make_request(endpoint)
    
#     def get_profile_all_actors(self, csv_file: csv):
#             ids, names, birth = extract_infos(csv_file=csv_file)

#             Profiles = []
#             for id, name, birth in zip(ids, names, birth):

#                 with open(f"{name}.json", "r", encoding="utf-8") as file:
#                     # load file
#                     json_file = json.load(file) 
#                     # Extract bio
#                     actor_bio = json_file["data"]["name"]["bio"]["text"]["plainText"]
#                     actor_dic = {
#                         "ID": id,
#                         "Name": name,
#                         "Birthdate": birth,
#                         "Biography": actor_bio
#                     }
#                 Profiles.append(actor_dic)
#         # Show profile Details
#             for profile in Profiles:
#                 for p in profile.items():
#                     print(f"{p}\n")

#     def get_all_celeb_awards(self, csv_file: csv):
#         """Displays all Actor Awards

#         Args:
#             csv_file (csv): Lists all Actors
#         """
#         ids, names, birth = extract_infos(csv_file=csv_file)
#         Awards = []
#         for id, name, birth in zip(ids, names, birth):
#             actor_filename = f"Award_{name}.json"
#             with open(actor_filename , "r", encoding="utf-8") as file:
#                 # load file
#                 jf = json.load(file) 
#                 award_data = jf["data"]["name"]["awardNominations"]
#                 awardNominations = award_data["total"]
#                 award_list = []
#                 for node in award_data["edges"]:
#                     if node["node"]["isWinner"] == True:
#                         award_list.append([node["node"]["award"]["awardName"], node["node"]["award"]["eventEdition"]["year"]])
#                 award_dict = {
#                     "actor_id": id, 
#                     "actor_name": name,
#                     "actor_nominations": awardNominations,
#                     "awards": award_list
#                 }    
#                 Awards.append(award_dict)
#         for award in Awards:
#             for key, value in award.items():
#                 print(f"{key}: {value}")

#     def get_actor_award(self, name):
#         """This function retrieves the awards of a given Actor. 

#         Args:
#             name (string): Name of the Actor

#         Returns:
#             dict: Dictionary with the total award anominations and a list of worn awards
#         """
#         jfile = f"{name}.json"
#         with open(jfile, "r", encoding="utf-8") as file:
#             jf = json.load(file)
#             award_data = jf["data"]["name"]["awardNominations"]
#             awardNominations = award_data["total"]
#             award_list = []
#             for node in award_data["edges"]:
#                 if node["node"]["isWinner"] == True:
#                     award_list.append([node["node"]["award"]["awardName"], node["node"]["award"]["eventEdition"]["year"]])
#             award_dict = {
#                 "actor_nominations": awardNominations,
#                 "awards": award_list
#             }   
#         return award_dict
            
        
        
#     # Functional Methods
#     def create_json_file(self, imdb_id="nm5097044", save_path="actor_meta_data.json", infos="meta"):
#         """Retrieve actor's metadata  or award and save results in a JSON file."""
#         if infos == "meta":
#             endpoint = f"/actors/v2/get-meta-data?nconsts={imdb_id}%2C{imdb_id}&first=20&country=US&language=en-US"
#         elif infos == "award":
#             endpoint = f"api/actors/get-awards?nm={imdb_id}&limit=25"
#         elif infos == "popular":
#             endpoint = f"/api/actors/get-most-popular?limit=25"
#         elif infos == "movies":
#             endpoint = f"/api/actors/get-known-for?limit=25&nm={imdb_id}"
#         elif infos == "bio":
#             endpoint = f"/api/actors/get-bio?nm={imdb_id}"
            
#         data = self._make_request(endpoint)
#         # Save the data to a JSON file
#         if os.path.exists(save_path):
#             return f"Die Datei {save_path} existiert bereits."
#         with open(save_path, "w", encoding="utf-8") as file:
#             json.dump(data, file, indent=4, ensure_ascii=False)
#         return f"Movies were loaded to a JSON file: {save_path}"
    
#     def get_list_of_most_popular_celeb(self, csv_file: csv):      
#         # Using Endpoint is depreciated
#         # endpoint = f"/api/actors/get-most-popular?limit=25"
#         # actors = self._make_request(endpoint)
#         # actor_ids = [actor.replace("/name/", "").strip("/") for actor in actors]
#         """This function loads a csv file to extract the ids, names and birthdays of the most popular actors and then stores them in lists
#         Args:
#             csv_file (csv): Contains the list of the 50 most popular celebrities
#         Returns:
#             List: A tupel of lists Actor's IDs, Name and birthdate
#         """    
#         lines = []
#         ids = []
#         names =[]
#         birthdates = []
#         i = 1
#         with open( csv_file, mode="r") as file:
#             csvfile = csv.reader(file)
            
#             # find the number of columns
#             headers = len(next(csvfile))
                    
#             for line in csvfile:
#                 lines.append(line)      
#         if headers <= 3:
#             for i in range(len(lines)):
#                 ids.append(lines[i][0])
#                 names.append(lines[i][1])
#                 birthdates.append(lines[i][2])
#         elif headers > 3:
#             # Extract idis from file 
#             for i in range(len(lines)):
#                 ids.append(lines[i][1])
#                 names.append(lines[i][5])
#                 birthdates.append(lines[i][7])
#         return ids, names, birthdates

    
#     def extract_celeb_infos(self, imdb_id, info_type):
#         if info_type == "bio": 
#             return self.get_actor_biography(name=imdb_id)

    

# #####################################################################################################################   

