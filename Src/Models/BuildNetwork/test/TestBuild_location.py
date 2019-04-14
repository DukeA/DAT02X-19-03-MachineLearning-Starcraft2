import unittest

from Models.BuildNetwork.BuildFacade import Build_location



class test_buildFacade(unittest.TestCase):

    """
        Test the build_location to get the right value
    """
    def test_getlist_coordionate(self):
        value = 2000 % 82
        index =34
        list_value = Build_location.get_location_in_list(self,value, index)
        should_be = (2000 % 82) * 82 + 34
        assert list_value == should_be


