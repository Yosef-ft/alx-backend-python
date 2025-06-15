'''
Unit test for utils 
'''
import unittest
from utils import *
from parameterized import parameterized
from typing import (
    Mapping,
    Sequence,
    Any,
    Dict,
    Callable,
)


class TestAccessNestedMap(unittest.TestCase):
    '''
    Class to test access nested map
    '''
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self,nested_map: Mapping, path: Sequence,expected_output):
        '''
        Function to test access_nested_map from utils
        '''
        result = access_nested_map(nested_map, path)
        self.assertEqual(result, expected_output)



if __name__ == '__main__':
    unittest.main()        