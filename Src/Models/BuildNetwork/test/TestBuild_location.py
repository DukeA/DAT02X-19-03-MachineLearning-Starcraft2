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
        assert len(n_list) == 1
        assert n_list == [(81, 81, 0)]

    """
        An method for testing to get a good location
    """

    def test_good_location(self):
        list = [(81, 51, 0)]
        n_list = Build_location.get_good_points(self, list)
        assert len(n_list) == 1
        assert n_list == [(81, 51, 0)]

    """
           An method for testing to get a good location
       """

    def test_good_location(self):
        list = [(41, 51, 0)]
        n_list = Build_location.get_good_points(self, list)
        assert len(n_list) == 1
        assert n_list == [(41, 51, 0)]

    """
        Test for if the method should be empty
    """

    def test_location_for_which_aint_valid(self):
        list = [(-1, -1, 0)]
        n_build_list = Build_location.get_good_points(self, list)
        assert len(n_build_list) == 0
        assert n_build_list == []

        """
            Test for if the method should be empty
        """

    def test_location_for_which_aint_valid(self):
        list = [(-1, 81, 0)]
        n_build_list = Build_location.get_good_points(self, list)
        assert len(n_build_list) == 0
        assert n_build_list == []

    """
        Test for border cases on the environment
    """

    def test_location_for_which_aint_valid(self):
        list = [(-1, 81, 0)]
        n_build_list = Build_location.get_good_points(self, list)
        assert len(n_build_list) == 0
        assert n_build_list == []

    """
        Test to get the best location from an list of  postions
    """

    def test_get_biggest_areas(self):
        list = [(40, 51, 0), (51, 40, 1), (60, 40, 2), (60, 40, 3)]
        n_build_list = Build_location.get_build_areas(self, list)
        assert len(0) == 2
        assert n_build_list == [(60, 40, 2), (60, 40, 3)]
