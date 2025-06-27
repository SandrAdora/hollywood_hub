import unittest 
from module_applayer import actor_profile


class TestDisplayActorProfile(unittest.TestCase):
    
    def test_display_actor_found(self):
        print("Start actor_profile test\n")
        """This is a testcase that returns OK when Actor could be found"""
        actor_ = actor_profile("Johnny Depp")
        if actor_  :
            actor_name = actor_[0]["actor_name_profile"]
            birthdate = actor_[0]["birthdate_profile"]
            self.assertIsNotNone(actor_name)
            print(actor_name)
            print(birthdate)
            print("Test ran successfully\n")
        print("Finish actor_profile test\n")
        

    def test_display_actor_not_found(self):
        print("Start actor_profile negative test\n")
        """This test checks behavior when an unknown actor is requested"""

        actor_ = actor_profile("Mystery Star Who Doesn't Exist")

        # Expecting None or empty list as a signal the actor wasn't found
        self.assertTrue(actor_ is None or len(actor_) == 0, "Expected no actor profile to be returned.")

        print("No actor found, as expected.\n")
        print("Finish actor_profile negative test\n")




if __name__=='__main__':
    unittest.main()
