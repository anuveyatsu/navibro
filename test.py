""" This file contains tests for app.py """
import unittest
from app import *
import vcr
from flask_testing import TestCase

class FlaskTestCase(TestCase):
    """ These are unit tests. """
    def create_app(self):
        """ This method is a part of flask_testing extension's requirement """
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app
    def test_home(self):
        """ Testing that root page set up correctly, should return 200 as status_code """
        response = app.test_client().get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
    def test_home_page_loads(self):
        """ Testing if root page loads correctly with right message """
        response = app.test_client().get('/', content_type='html/text')
        self.assertTrue(b'Hi there! Go to "/navigator" and pass "search_term" parameter'
                        in response.data)
    def test_navigator(self):
        """ Testing that navigator page set up correctly, should return 200 as status_code """
        response = app.test_client().get('/navigator', content_type='html/text')
        self.assertEqual(response.status_code, 200)
    def test_navigator_page_loads(self):
        """ Testing that navigator page returns correct message if search_term wasn't provided """
        response = app.test_client().get('/navigator', content_type='html/text')
        self.assertTrue(b'provide a search_term' in response.data)
    @vcr.use_cassette('fixtures/vcr_cassettes/synopsis.yaml')
    def test_navigator_with_search_term_data_type(self):
        """ Testing navigator if it passes data of expected type to template """
        response = app.test_client().get('/navigator',
                                         query_string=dict(search_term='testtest'),
                                         content_type='html/text')
        self.assertTrue(isinstance(self.get_context_variable('data'), list))
    @vcr.use_cassette('fixtures/vcr_cassettes/synopsis.yaml')
    def test_navigator_with_search_term_data_length(self):
        """ Testing navigator if it passes data of correct length """
        response = app.test_client().get('/navigator',
                                         query_string=dict(search_term='testtest'),
                                         content_type='html/text')
        self.assertTrue(len(self.get_context_variable('data')) == 5)
    @vcr.use_cassette('fixtures/vcr_cassettes/synopsis.yaml')
    def test_navigator_with_search_term_data_has_name(self):
        """ Testing navigator if it passes data that contains 'name' key """
        response = app.test_client().get('/navigator',
                                         query_string=dict(search_term='testtest'),
                                         content_type='html/text')
        self.assertTrue('name' in self.get_context_variable('data')[0])
    @vcr.use_cassette('fixtures/vcr_cassettes/synopsis.yaml')
    def test_navigator_with_search_term_data_has_created_at(self):
        """ Testing navigator if it passes data that contains 'created_at' key """
        response = app.test_client().get('/navigator',
                                         query_string=dict(search_term='testtest'),
                                         content_type='html/text')
        self.assertTrue('created_at' in self.get_context_variable('data')[0])
    @vcr.use_cassette('fixtures/vcr_cassettes/synopsis.yaml')
    def test_navigator_with_search_term_data_has_owners_info(self):
        """ Testing navigator if it passes data that contains owner's info """
        response = app.test_client().get('/navigator',
                                         query_string=dict(search_term='testtest'),
                                         content_type='html/text')
        self.assertTrue('owner' in self.get_context_variable('data')[0])
    @vcr.use_cassette('fixtures/vcr_cassettes/synopsis.yaml')
    def test_navigator_with_search_term_data_has_sha(self):
        """ Testing navigator if it passes data that contains 'sha' key """
        response = app.test_client().get('/navigator',
                                         query_string=dict(search_term='testtest'),
                                         content_type='html/text')
        self.assertTrue('sha' in self.get_context_variable('data')[0])
    @vcr.use_cassette('fixtures/vcr_cassettes/synopsis.yaml')
    def test_navigator_with_search_term_data_has_commit_message(self):
        """ Testing navigator if it passes data that contains 'commit_message' key """
        response = app.test_client().get('/navigator',
                                         query_string=dict(search_term='testtest'),
                                         content_type='html/text')
        self.assertTrue('commit_message' in self.get_context_variable('data')[0])
    @vcr.use_cassette('fixtures/vcr_cassettes/synopsis.yaml')
    def test_navigator_with_search_term_data_has_commit_author_name(self):
        """ Testing navigator if it passes data that contains 'commit_author_name' key """
        response = app.test_client().get('/navigator',
                                         query_string=dict(search_term='testtest'),
                                         content_type='html/text')
        self.assertTrue('commit_author_name' in self.get_context_variable('data')[0])
    @vcr.use_cassette('fixtures/vcr_cassettes/synopsis.yaml')
    def test_navigator_with_search_term_correct_message(self):
        """ Testing navigator page if loads correct message """
        response = app.test_client().get('/navigator',
                                         query_string=dict(search_term='testtest'),
                                         content_type='html/text')
        assert b'You searched for: testtest' in response.data

    def test_navigator_with_empty_search_term(self):
        """ Testing how app behaves when search_term is given as empty string """
        response = app.test_client().get('/navigator',
                                         query_string=dict(search_term=''),
                                         content_type='html/text')
        assert b'provide a search_term' in response.data

    @vcr.use_cassette('fixtures/vcr_cassettes/synopsis2.yaml')
    def test_github_repo_method_data_type(self):
        """ Testing github_repo method if it returns expected json data
        when valid search_term is passed """
        response = github_repo('testtest')
        self.assertTrue(isinstance(response, dict))
    @vcr.use_cassette('fixtures/vcr_cassettes/synopsis2.yaml')
    def test_github_repo_method_data_length(self):
        """ Testing github_repo method if it returns expected length of data """
        response = github_repo('testtest')
        self.assertTrue(len(response) == 3)
    @vcr.use_cassette('fixtures/vcr_cassettes/synopsis2.yaml')
    def test_github_repo_method_has_total_count(self):
        """ Testing github_repo method if data it returns has 'total_count' key """
        response = github_repo('testtest')
        self.assertTrue('total_count' in response)
    @vcr.use_cassette('fixtures/vcr_cassettes/synopsis2.yaml')
    def test_github_repo_method_incomplete_results(self):
        """ Testing github_repo method
        if data it returns has 'incomplete_results' key that is False """
        response = github_repo('testtest')
        self.assertTrue(response['incomplete_results'] is False)
    @vcr.use_cassette('fixtures/vcr_cassettes/synopsis2.yaml')
    def test_github_repo_method_has_items(self):
        """ Testing github_repo method if its response has 'items' key """
        response = github_repo('testtest')
        self.assertTrue('items' in response)

    @vcr.use_cassette('fixtures/vcr_cassettes/synopsis3.yaml')
    def test_github_repo_method_with_empty(self):
        """ Testing github_repo method when empty search_term is passed """
        response = github_repo('')
        self.assertTrue('try again' in response)

    @vcr.use_cassette('fixtures/vcr_cassettes/synopsis4.yaml')
    def test_github_commits_method_data_type(self):
        """ Testing github_commits method if it returns expected data type """
        response = github_commits('TestTestOrgOrg/testtest')
        self.assertTrue(isinstance(response, dict))
    @vcr.use_cassette('fixtures/vcr_cassettes/synopsis4.yaml')
    def test_github_commits_method_has_sha(self):
        """ Testing github_commits method if data it returns has 'sha' key """
        response = github_commits('TestTestOrgOrg/testtest')
        self.assertTrue('sha' in response)
    @vcr.use_cassette('fixtures/vcr_cassettes/synopsis4.yaml')
    def test_github_commits_method_has_commit(self):
        """ Testing github_commits method if data it returns has 'commit' key """
        response = github_commits('TestTestOrgOrg/testtest')
        self.assertTrue('commit' in response)

    @vcr.use_cassette('fixtures/vcr_cassettes/synopsis5.yaml')
    def test_github_commits_method_wrong_path(self):
        """ Testing github_commits method with wrong path """
        response = github_commits('TestTestOrgOrg')
        self.assertTrue(response == 'n/a')

    def test_sort_desc_method(self):
        """ Testing the method takes a list of dictionaries and a term,
        then returns sorted list by given term in descending order """
        data = [{'term':1}, {'term':0}, {'term':8}]
        sorted_data = [{'term':8}, {'term':1}, {'term':0}]
        response = sort_desc(data, 'term')
        self.assertEqual(response, sorted_data)

    def test_first_5_items_method(self):
        """ Testing the method takes a list and returns its first 5 items """
        data = [2, 6, 45, 0, 11, 9]
        first_5_data = [2, 6, 45, 0, 11]
        response = first_5_items(data)
        self.assertEqual(response, first_5_data)

if __name__ == '__main__':
    unittest.main()
