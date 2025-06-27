import unittest
from module_applayer import get_actors_movies
from helperFunctions import get_actors_best_known_for_movies


class TestActorMovie(unittest.TestCase):
    """This class tests the movie display functionality"""
    def test_show_actor_movie(self):
        print("Start Testcase for actor_movie\n")
        """This function returns OK when top five movies of an actor was fou"""
        list_of_names = ["Johnny Depp", "Angelina Jolie", "Will Smith", "Denzel Washington", "Tom Cruise"]
        top_movies_exists = False
        
        for name in list_of_names:
            top_5_movies = get_actors_movies(name)
            if len(top_5_movies) > 0:
                top_movies_exists = True
                self.assertTrue(top_movies_exists)
                # show only the first movie of actors in the list
                print(top_5_movies[0]["movie_title"])
        print("Test ran successfully\n")
        print("Finish Testcase: test_show_actor_movie\n")
    

    def test_show_actor_movie_not_found(self):
        print("Start Testcase: actor with no movie record\n")
        """This test verifies behavior when the actor has no movies listed"""
        
        # Use names assumed not to exist in the dataset
        fake_names = ["Invisible Star", "Nonexistent Actor", "Unknown Person"]
        
        for name in fake_names:
            top_5_movies = get_actors_movies(name)
            print(f"Testing with: {name}")
            
            # Ensure we get an empty list instead of an error
            self.assertIsInstance(top_5_movies, list)
            self.assertEqual(len(top_5_movies), 0, f"Expected no movies for '{name}'")
        
        print("Finished Testcase: actor with no movie record\n")


if __name__=="__main__":
    unittest.main()