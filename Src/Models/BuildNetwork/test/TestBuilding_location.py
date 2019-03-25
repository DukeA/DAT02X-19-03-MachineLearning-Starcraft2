

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
        list = BuildModelLocations.set_building_location(self,list)
        assert list[20][20] == 10
        print("The value changed")





