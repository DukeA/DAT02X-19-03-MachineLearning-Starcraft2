

import unittest

from Models.BuildNetwork.BuildModelLocations import  BuildModelLocations
import numpy as np
import numpy.testing as npt


class test_build_location(unittest.TestCase):

    def testStrucutureModuel(self):
        x = 82
        y = 82
        list = BuildModelLocations.set_buildlocations(self)
        assert len(list) == x
        assert len(list[0]) == y
        list_2 = np.full((82, 82), 0)
        npt.assert_array_equal(list, list_2)
        print("The size is the same")

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
        list = BuildModelLocations.set_building_location(self ,list)
        assert list[20][20] == 10
        print("The value changed")

    def test_check_the_start_location(self):
        x = 82
        y = 82
        list = BuildModelLocations.set_buildlocations(self)
        for i in range(41,44):
            for j in range(41,44):
                list[i][j] = 345
        assert len(list) == x
        assert len(list[0]) == y
        assert BuildModelLocations.check_startLocation_Of_Base(self, list) == True
        print("The value was passed")

    def test_check_start_location_to_be_false(self):
        x = 82
        y = 82
        list = BuildModelLocations.set_buildlocations(self)
        for i in range(21,24):
            for j in range(21,24):
                list[i][j] = 345
        assert len(list) == x
        assert len(list[0]) == y
        assert BuildModelLocations.check_startLocation_Of_Base(self,list) == False
        print("The value did returned false")

    def test_check_value_of_map_to_be_the_other(self):
        x = 82
        y = 82
        list = BuildModelLocations.set_buildlocations(self)
        for i in range(21, 24):
            for j in range(21, 24):
                list[i][j] = 345
        assert len(list) == x
        assert len(list[0]) == y
        list2 = BuildModelLocations.set_building_location(self,list)
        value = list2
        npt.assert_array_equal(list2,value)
        assert list2[41][20] == 5
        assert list2[60][60] == 10
        assert list2[31][60] == 5
        print("The value returned correct")


    def test_check_value_of_map_to_be_other(self):
        x = 82
        y = 82
        list = BuildModelLocations.set_buildlocations(self)
        for i in range(41, 44):
            for j in range(41, 44):
                list[i][j] = 345
        assert len(list) == x
        assert len(list[0]) == y
        list2 = BuildModelLocations.set_building_location(self,list)
        value = list2
        npt.assert_array_equal(list2,value)
        assert list2[0][20] == 10
        assert list2[41][60] == 5
        assert list2[81][30] == 5
        print ("The value is correct for the given output")









