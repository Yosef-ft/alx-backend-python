#!/usr/bin/env python3
'''
Test for client.py
'''

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from utils import *
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    '''
    Class to test GithubOrgClient class
    '''

    @parameterized.expand([
        ('google',),
        ('abc',)
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        '''
        function to test GithubOrgClient.org
        '''

        expected_payload = {"payload": True}

        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        response = client.org

        self.assertEqual(response, expected_payload)

        expected_url = "https://api.github.com/orgs/{}".format(org_name)
        mock_get_json.assert_called_once_with(expected_url)

    @parameterized.expand([
        ('google',),
        ('abc',)
    ])
    def test_public_repos_url(self, org_name):
        '''
        Test the implementation of _public_repos_url
        '''
        with patch.object(GithubOrgClient, 'org',
                          new_callable=PropertyMock) as mock_org:

            expected_url = f"https://api.github.com/orgs/{org_name}/repos"
            mock_payload = {"repos_url": expected_url}

            mock_org.return_value = mock_payload

            client = GithubOrgClient(org_name)
            response = client._public_repos_url

            self.assertEqual(response, expected_url)

    @parameterized.expand([
        ('google'),
        ('abc')
    ])
    @patch('client.get_json')
    def test_public_repos(self, org_name, mock_get_json):
        '''
        Test public repos
        '''
        with patch.object(GithubOrgClient, '_public_repos_url',
                          new_callable=PropertyMock) as mock_public_repos_url:

            expected_url = f"https://api.github.com/orgs/{org_name}/repos"
            value_public_repos = [
                {"name": "repo1"},
                {"name": "repo2"},
            ]
            mock_get_json.return_value = value_public_repos

            client = GithubOrgClient(org_name)
            response = client.public_repos()

            self.assertEqual(response, ['repo1', 'repo2'])

            mock_public_repos_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, license_value):
        '''
        Test has license function
        '''

        license = GithubOrgClient.has_license(repo, license_key)

        self.assertEqual(license, license_value)


if __name__ == '__main__':
    unittest.main()
