
import unittest

from Models.BuildNetwork.BuildModelGather import BuildModelGather
import numpy as np
import numpy.testing as npt


class test_build_model(unittest.TestCase):

        def testModule(self):
            x = 82
            y = 82
            list = BuildModelGather.set_buildmap(self)
            assert len(list) == x
            assert len(list[0]) == y
            _list = np.full((81, 81), 0)
            npt.assert_array_equal(list, _list)
            print("Test Size being Created to true")

        def test_buildModule(self):
            x = 3
            y = 3
            unit_shape = 3
            type = 1
            list2 = BuildModelGather.set_setsourdingvalues(self, x, y, unit_shape, type)
            value = len(list2)
            assert value == x*y
            value2 = len(list2[0])
            assert value2 == y
            list3 = [(0, 0, 1), (0, 1, 1), (0, 2, 1), (1, 0, 1), (1, 1, 1), (1, 2, 1), (2, 0, 1), (2, 1, 1), (2, 2, 1)]
            npt.assert_array_almost_equal(list2,list3)
            print("The arrays are equal to each other")

        def test_build_sourndings(self):
            x = 1
            y = 1
            unit_shape = 1
            type = 1
            list = BuildModelGather.set_setsourdingvalues(self, x, y, unit_shape, type)
            list_value = len(list)
            assert list_value == x*y
            list_value2 = len(list[0])
            assert list_value2 == 3
            list_value3 = [(0, 0, 1)]
            npt.assert_array_almost_equal(list, list_value3)
            print("The arrays are equal to each other")






if __name__=='__main__':
    unittest.main()