import unittest

from Models.BuildNetwork.BuildFacade import BuildFacade
from Models.BuildNetwork.BuildModelLocations import BuildModelLocations
import numpy as np
import numpy.testing as npt
import random


class test_buildFacade(unittest.TestCase):

    """
        The Method tests the build facade method
        for the print enviorment
    """
    def test_print_enviorment(self):
        value = 82*82
        list = []
        for i in range(value):
            list.append(random.randint(0,1))
        assert len(list) == value
        BuildFacade.print_enviroment(self,list)

    """
        The test method for the stacking value in the  build Facade
    """
    def test_stacked_value(self):
        list=[1]
        n_list = BuildFacade.stacked_enviorment(self,list)
        assert len(list) == 4



    """
        Test the method for getting a good build location
    """
    def test_build_model(self):
        n_list = np.full((82, 82), 0)
        for i in range(41, 44):
            for j in range(41, 44):
                n_list[i][j] = 345
        list = BuildModelLocations.set_building_location(self,n_list)
        n_list = BuildFacade.build_model(self,list)
        assert len(list) == 3
        for list_value in n_list:
            assert len(n_list[list_value]) == 3

    """
          The test method checks if it is able to 
          flatten the value into a single list 
    """

    def test_check_value_of_map_to_be_single(self):
        list = [[1, 3, 4], [2, 3, 5]]
        n_list = BuildFacade.flatten_values(self, list)
        assert n_list == [1, 3, 4, 2, 3, 5]
        print("The value was then flattend")

    """
        Check the for certain  
        bordercase on flattend
    """

    def test_method_to_be_empty(self):
        list = [[], []]
        n_list = BuildFacade.flatten_values(self, list)
        assert n_list == []
        print("The value for the list is an empty list")

    """
        Check borderCase if there is  
        a single element in the arrays
    """

    def test_method_if_list_if_the_method_is_one(self):
        list = [[1], [1]]
        n_list = BuildFacade.flatten_values(self, list)
        assert n_list == [1, 1]
        print("The list is of same size ")

    """
        Check if the size of the arrays is of uneven size 
    """

    def test_flatten_uneven_length(self):
        list = [[1, 2, 3], [1, 2]]
        n_list = BuildFacade.flatten_values(self, list)
        assert n_list == [1, 2, 3, 1, 2]
        print("The list is the flatten")

    """
        Check if the  list is other arrat is uneven.
    """

    def test_the_flatte_uneven_length(self):
        list = [[1, 2], [1, 2, 3]]
        n_list = BuildFacade.flatten_values(self, list)
        assert n_list == [1, 2, 1, 2, 3]
        print("Value did change")
