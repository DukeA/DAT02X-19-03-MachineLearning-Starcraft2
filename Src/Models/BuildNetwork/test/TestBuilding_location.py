import unittest

from Models.BuildNetwork.BuildModelLocations import BuildModelLocations
import numpy as np
import numpy.testing as npt


class test_build_location(unittest.TestCase):
    """
        An test to check the value actually is of the size 82,82
    """

    def testStrucutureModuel(self):
        x = 82
        y = 82
        list = BuildModelLocations.set_buildlocations(self)
        assert len(list) == x
        assert len(list[0]) == y
        list_2 = np.full((82, 82), 0)
        npt.assert_array_equal(list, list_2)
        print("The size is the same")

    """
        Test Method to se that the value is changed on the location where it can build.
    """

    def test_valuesSetModuel(self):
        x = 82
        y = 82
        list = BuildModelLocations.set_buildlocations(self)
        for i in range(41, 44):
            for j in range(41, 44):
                list[i][j] = 345
        assert len(list) == x
        assert len(list[0]) == y
        assert list[41][43] == 345
        assert list[20][20] != 10
        list = BuildModelLocations.set_building_location(self, list)
        assert list[20][20] == 10
        print("The value changed")

    """
        Test method to see that the location is set correctly where the base is located
    """

    def test_check_the_start_location(self):
        x = 82
        y = 82
        list = BuildModelLocations.set_buildlocations(self)
        for i in range(41, 44):
            for j in range(41, 44):
                list[i][j] = 345
        assert len(list) == x
        assert len(list[0]) == y
        assert BuildModelLocations.check_startLocation_Of_Base(self, list) == True
        print("The value was passed")

    """
           Test method to see that the location is on another place
    """

    def test_check_start_location_to_be_false(self):
        x = 82
        y = 82
        list = BuildModelLocations.set_buildlocations(self)
        for i in range(21, 24):
            for j in range(21, 24):
                list[i][j] = 345
        assert len(list) == x
        assert len(list[0]) == y
        assert BuildModelLocations.check_startLocation_Of_Base(self, list) == False
        print("The value did returned false")

    """
           Test method to see that the location is set of the values are set on the correct place
    """

    def test_check_value_of_map_to_be_the_other(self):
        x = 82
        y = 82
        list = BuildModelLocations.set_buildlocations(self)
        for i in range(21, 24):
            for j in range(21, 24):
                list[i][j] = 345
        assert len(list) == x
        assert len(list[0]) == y
        list2 = BuildModelLocations.set_building_location(self, list)
        value = list2
        npt.assert_array_equal(list2, value)
        assert list2[41][20] == 5
        assert list2[60][60] == 10
        assert list2[31][60] == 5
        print("The value returned correct")

    """
        Test method to see that the location is set of the values where it is okey to build have been set
    """

    def test_check_value_of_map_to_be_other(self):
        x = 82
        y = 82
        list = BuildModelLocations.set_buildlocations(self)
        for i in range(41, 44):
            for j in range(41, 44):
                list[i][j] = 345
        assert len(list) == x
        assert len(list[0]) == y
        list2 = BuildModelLocations.set_building_location(self, list)
        value = list2
        npt.assert_array_equal(list2, value)
        assert list2[0][20] == 10
        assert list2[41][60] == 5
        assert list2[81][30] == 5
        print("The value is correct for the given output")

    """
        The test method checks if it is able to 
        flatten the value into a single list 
    """


    def test_check_value_of_map_to_be_single(self):
        list = [[1, 3, 4], [2, 3, 5]]
        n_list = BuildModelLocations.flatten_values(self, list)
        assert n_list == [1, 3, 4, 2, 3, 5]
        print("The value was then flattend")

    """
        Check the for certain  
        bordercase on flattend
    """
    def test_method_to_be_empty(self):
        list = [[], []]
        n_list = BuildModelLocations.flatten_values(self, list)
        assert n_list == []
        print("The value for the list is an empty list")


    """
        Check borderCase if there is  
        a single element in the arrays
    """


    def test_method_if_list_if_the_method_is_one(self):
        list = [[1], [1]]
        n_list = BuildModelLocations.flatten_values(self, list)
        assert n_list == [1, 1]
        print("The list is of same size ")


    """
        Check if the size of the arrays is of uneven size 
    """
    def test_flatten_uneven_length(self):
        list = [[1, 2, 3], [1, 2]]
        n_list = BuildModelLocations.flatten_values(self, list)
        assert n_list == [1, 2, 3, 1, 2]
        print("The list is the flatten")


    """
        Check if the  list is other arrat is uneven.
    """
    def test_the_flatte_uneven_length(self):
        list =[[1,2],[1,2,3]]
        n_list = BuildModelLocations.flatten_values(self,list)
        assert n_list ==[1,2,1,2,3]
        print("Value did change")
