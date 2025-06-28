import unittest

from module_applayer import get_actor_awards

class TestActorAward(unittest.TestCase):

    def test_get_actor_awards(self):
        print("Start Get actor awards test case\n")

        name = "Johnny Depp"
        result = get_actor_awards(name=name)
        self.assertTrue(isinstance(result, list), "Expected result to be a list.")
        # Optionally check if list has content and correct keys
        for award in result:
            self.assertIn("award_name", award)
            self.assertIn("award_year", award)
            print(award)
        print("Finish Get actor awards test case\n")
        
    def test_get_actor_awards_empty(self):
        print("\nStart test case: get_actor_awards with actor who has no awards\n")

        name = "Unfamous Person"  # Assuming this name isn't in the dataset
        result = get_actor_awards(name=name)

        self.assertTrue(isinstance(result, list), "Expected a list even if it's empty.")
        self.assertEqual(len(result), 0, "Expected the list to be empty for an unknown actor.")
        
        print("Returned:", result)
        print("\nFinish test case: get_actor_awards with actor who has no awards\n")

if __name__ == "__main__":
    unittest.main()
