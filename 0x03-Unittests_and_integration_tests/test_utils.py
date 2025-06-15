'''
Unit test for utils 
'''
import unittest
from utils import *
from parameterized import parameterized
from unittest.mock import patch, MagicMock
import requests
import json
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


class TestGetJson(unittest.TestCase):
    '''
    Class to test get json
    '''
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    @patch('requests.get')
    def test_get_json(self, test_url, test_payload, mock_request):

        mock_request.return_value.json.return_value = test_payload

        payload = get_json(test_url)
        self.assertEqual(payload, test_payload)



if __name__ == '__main__':
    unittest.main()        