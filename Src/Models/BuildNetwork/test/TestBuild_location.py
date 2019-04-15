import unittest

from Models.BuildNetwork.BuildFacade import Build_location


class test_buildFacade(unittest.TestCase):
    """
        Test the build_location to get the right value
    """

    def test_getlist_coordionate(self):
        value = 2000 % 82
        index = 34
        list_value = Build_location.get_location_in_list(self, value, index)
        should_be = (2000 % 82) * 82 + 34
        assert list_value == should_be

    """
        An method for testing to get a good location
    """

    def test_good_locations(self):
        list = [(81, 81, 0)]
        n_list = Build_location.get_good_points(self, list)
        assert len(n_list) == 0
        assert n_list == []

    """
        An method for testing to get a good location
    """

    def test_good_location(self):
        list = [(81, 51, 0)]
        n_list = Build_location.get_good_points(self, list)
        assert len(n_list) == 0
        assert n_list == []

    """
           An method for testing to get a good location
       """

    def test_good_location(self):
        list = [(41, 51, 0)]
        n_list = Build_location.get_good_points(self, list)
        assert len(n_list) == 1
        assert n_list == [(41, 51, 0)]