
import unittest

from Models.BuildNetwork.BuildModelGather import BuildModelGather
import numpy as np
import numpy.testing as npt


class TestSuite(unittest.TestCase):

        def testModule(self):
            x = 81
            y = 81
            list = BuildModelGather.set_buildmap(self)
            assert len(list) == x
            assert len(list[0]) == y
            _list = np.full((81, 81), 0)
            npt.assert_array_equal(list, _list)
            print("Test Size being Created to true")










if __name__=='__main__':
    unittest.main()