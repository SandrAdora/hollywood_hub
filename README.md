
# Hollywood Actors and Actresses API-Driven Project 

## Project Overview 

This project is a python-based application that provides information about the top 50 most popular Hollywood actors and actresses using the API-driven backend and a SQL_Lite database. 

## Features

1. List of top 50 popular Actors and Actresses
2. Celebrity Biography and Birth year
3. Movie Details 
4. Awards Information 
5. Database storage for Fast data Access 
6. User-Friendly Web Interface
7. FastAPI Backend with IMDb API integration 

## Project Structure 

hollywood_hub/
├── data
│   ├── celebrities_in_json  # Stores all celebrity infos as json file
│   ├── images               # Stores Celebrity images as jpg files aswell as movie images of all movies 
├── documentation
│   ├── testing
│   ├──│   ├── testcase_actor_movie.png
│   ├──│   ├── testcase_actor_profile.png
│   ├──│   ├── testcase_awards.png
│   ├── hollywood_hub.drawio.html
│   ├── hollywood_hub.drawio.png
│   ├── application_running.svg
├── testing
│   ├── test_applayer.py    # Testing the processing module 
│   ├── test_databaselayer.py # Testing the database layer
│   ├── test_actor_awards.py
│   ├── test_actor_movie.py
│   ├── test_actore_profile.py
├── __init__.py
├── applayer.ipynb           # Business logic, communicates with the front and backend
├── celeb.db                 # Database        
├── databaselayer.ipynb      # Persistance layer communicates directly with the database  using FastAPI endpoints
├── databaseModels.py        # SQLAlchemy Models, used to create the database
├── helperFunctions.py       # Provides functions to run redundant tasks
├── models.py                # Pydantic models used to verify data input
├── README.md                # Project documentation
├── requirements.txt         # Requested packages




# Project Setup and Exceution Guide 

   1. ## Development Environment Preparation 
      
      - Ensure that yu have a suitable integrated development environment (IDE) installed. You may use Visual Studio Code (VSC) or any other highquality IDE for this project
      -  Install Python 3.13 or later version, along with pip, to proceed with installing *modules*/*packages* from the *requirements* file
     
   2. ## Virtual Environment Configuration 
      
      - This Step is not crucial, however to prevent confilicts with other python-packages in your system when installing, 
        1. create a virtual environment using the following command in your command-line interface *python -m venv <name_of_your_virt_folder>
        2. cd <name_of_your_virt_folder>/Scripts/activate
     
   3. ## Dependecy Intallation 
    
    - Install all required modules listed in the *requirements.txt*

   4. ## Project excecution 
    
        1.  Open the *databaselayer.ipynb*  and execute all its cells. Make sure all cells are ticked green and unvicorn is running. You should see this info: 
            ~. INFO:     Started server process [24540] # Or your port number
            INFO:     Waiting for application startup.
            INFO:     Application startup complete.
            INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)

        2.  Open the *applayer.ipynb*  and execute all its cells. Make sure  all cells are ticked green and there is a connection to the application. You should see this info or atleast no errors. 
        Note: the output below only appear ones when starting this project:
            ~.  Connecting to wss://anvil.works/uplink
                Anvil websocket open
                Connected to "Default Environment" as SERVER

 # Load the Application: 
        ~ To run the application: https://sleepy-royal-slice.anvil.app
        This software should open an run fine, when the **databaselayer.ipynb** and **applayer.ipynb** are running. If you encounter errors, please make sure both files are running.
  
   ## Navigating through Application 
    
    - Click on the actor's name to obtain detailed information 
    - Alternatively, manually enter the actor's name into the search field
    - If the name is misspelled, an error notification will be displayed
# Testing
    Before running test, please make sure the databaselayer.ipynb is running otherwise there will be an error
# Important Links for references

* FastAPI - SQLite Databases: https://www.geeksforgeeks.org/fastapi-sqlite-databases/
* SQLAlchemy: https://docs.sqlalchemy.org/en/14/orm/quickstart.html
* Anvil: https://anvil.works/blog/http-api-endpoints
* Image handling: https://pythonguides.com/python-save-an-image-to-file/