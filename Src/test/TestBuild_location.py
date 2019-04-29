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

    """
        Test method for the function
    """

    def test_build_placment(self):
        this_list = [[0, 0, 1, 0, 1],
                     [0, 1, 1, 1, 0],
                     [0, 1, 1, 1, 0],
                     [0, 1, 1, 1, 0],
                     [0, 0, 1, 0, 0]]
        n_build_list = Build_location.get_surronding_area(self, this_list)
        assert len(n_build_list) == 1

    """
        The test is for checking  if the space is not an weird figure 
    """

    def test_for_ordinary_build_placement(self):
        this_list = [[0, 0, 0, 0, 0],
                     [0, 1, 1, 1, 0],
                     [0, 1, 1, 1, 0],
                     [0, 1, 1, 1, 0],
                     [0, 0, 0, 0, 0]]
        n_build_list = Build_location.get_surronding_area(self, this_list)
        assert len(n_build_list) == 1

    """
        The test is for checking  space with two list with the same size
    """

    def test_method_for_build_placement_with_equalsize(self):
        this_list2 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 1, 1, 1, 0, 0, 1, 1, 1, 0],
                      [0, 1, 1, 1, 0, 0, 1, 1, 1, 0],
                      [0, 1, 1, 1, 0, 0, 1, 1, 1, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        n_build_list = Build_location.get_surronding_area(self, this_list2)
        assert len(n_build_list) == 2

    """
        Test method for multiple build placements
    """

    def test_method_for_multiple_build_placement(self):
        this_list3 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 1, 1, 1, 0, 0, 1, 1, 1, 0],
                      [0, 1, 1, 1, 0, 0, 1, 1, 1, 0],
                      [0, 1, 1, 1, 0, 0, 1, 1, 1, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 1, 1, 1, 0, 0, 1, 1, 1, 0],
                      [0, 1, 1, 1, 0, 0, 1, 1, 1, 0],
                      [0, 1, 1, 1, 0, 0, 1, 1, 1, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        n_build_list = Build_location.get_surronding_area(self, this_list3)
        assert len(n_build_list) == 4

    """
        Check for all uneven build_areas
    """

    def test_method_for_different_size(self):
        this_list4 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 1, 1, 1, 0, 0, 1, 1, 1, 0],
                      [0, 1, 1, 1, 0, 0, 1, 1, 1, 0],
                      [0, 1, 1, 1, 0, 0, 1, 1, 1, 0],
                      [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                      [0, 1, 1, 1, 0, 0, 1, 1, 1, 0],
                      [0, 1, 1, 1, 0, 0, 1, 1, 1, 0],
                      [0, 1, 1, 1, 0, 0, 1, 1, 1, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        n_build_list = Build_location.get_surronding_area(self, this_list4)
        assert len(n_build_list) == 3
        """
            Check for all uneven build_areas
        """

    def test_odd_size_location(self):
        this_list_odd = [[0, 0, 0, 0, 0],
                         [0, 1, 1, 1, 0],
                         [0, 1, 1, 1, 0],
                         [0, 1, 1, 1, 0],
                         [0, 1, 1, 1, 0],
                         [0, 1, 1, 1, 0],
                         [0, 1, 1, 1, 0],
                         [0, 1, 1, 1, 0],
                         [0, 0, 0, 0, 0]]
        n_build_list = Build_location.get_surronding_area(self, this_list_odd)
        assert len(n_build_list) == 1

    """
        Check for two even build areas with the same size
    """

    def test_method_for_different_size2(self):
        this_list4 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 1, 1, 0, 0, 0, 1, 1, 1, 0],
                      [0, 1, 1, 1, 0, 0, 1, 1, 1, 0],
                      [0, 1, 1, 1, 0, 0, 1, 1, 1, 0],
                      [0, 1, 1, 1, 0, 0, 1, 1, 1, 0],
                      [0, 1, 1, 1, 0, 0, 1, 1, 1, 0],
                      [0, 1, 1, 1, 0, 0, 1, 1, 1, 0],
                      [0, 1, 1, 1, 0, 0, 1, 1, 1, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        n_build_list = Build_location.get_surronding_area(self, this_list4)
        assert len(n_build_list) == 2

    """
        Check for the 
    """

    def test_method_for_different_size3(self):
        this_list4 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 1, 1, 1, 0, 0, 1, 1, 1, 0],
                      [0, 1, 1, 1, 0, 0, 1, 1, 1, 0],
                      [0, 1, 1, 1, 0, 0, 1, 1, 1, 0],
                      [0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
                      [0, 1, 1, 1, 0, 0, 1, 1, 1, 0],
                      [0, 1, 1, 1, 0, 0, 1, 1, 1, 0],
                      [0, 1, 1, 1, 0, 0, 1, 1, 1, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        n_build_list = Build_location.get_surronding_area(self, this_list4)
        assert len(n_build_list) == 3

        """
            The test method for checking uneven base location
        """

    def test_method_for_uneven_base1(self):
        test_list6 = [[0, 0, 0, 0, 0, 0, 0],
                      [0, 1, 1, 1, 1, 1, 0],
                      [0, 1, 1, 1, 1, 1, 0],
                      [0, 1, 1, 1, 1, 1, 0],
                      [0, 1, 1, 1, 1, 1, 0],
                      [0, 0, 0, 0, 0, 0, 0]]
        n_build_list = Build_location.get_surronding_area(self, test_list6)
        assert len(n_build_list) == 1

    """
        The test method for checking uneven base location
    """

    def test_method_for_uneven_base2(self):
        test_list6 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                      [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                      [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                      [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        n_build_list = Build_location.get_surronding_area(self, test_list6)
        assert len(n_build_list) == 1

    """
        The following method is an mock of how the environment looks like  for the testing  it.
    """

    def test_mock_for_Build_Placement(self):
        this_list5 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0],
                      [0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0],
                      [0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        n_build_list = Build_location.get_surronding_area(self, this_list5)
        assert len(n_build_list) == 7

    """
        Check if the build_location is empty 
    """

    def test_build_location_empty(self):
        this_build_area = [()]
        n_build_list = Build_location.build_location(self, this_build_area)
        assert len(n_build_list) == 0

    """
        Check if the following calculation is then all zeros
    """

    def test_build_location_zeros(self):
        this_build_area = [(0, 0, 0, 0)]
        n_build_list = Build_location.build_location(self, this_build_area)
        assert len(n_build_list) == 0

    """
        Get's the middle location for that possible point where  they can build
    """

    def test_gettting_middle_build_area(self):
        this_build_area = [(2, 2, 2, 2)]
        n_build_list = Build_location.build_location(self, this_build_area)
        assert len(n_build_list) == 1
        value = n_build_list[0]
        assert value == (1, 1, 4)

    """
        Get the position to the left of the 
    """
    def test_odd_build_areas(self):
        this_build_area = [(3, 3, 3, 3)]
        n_build_list = Build_location.build_location(self, this_build_area)
        assert len(n_build_list) == 1
        value = n_build_list[0]
        assert value == [(2, 2, 9)]
