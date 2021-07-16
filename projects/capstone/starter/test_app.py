import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Actor, Movie

casting_assistant_token = os.environ.get('CASTING_ASSISTANT_TOKEN')
casting_director_token = os.environ.get('CASTING_DIRECTOR_TOKEN')
executive_producer_token = os.environ.get('EXECUTIVE_PRODUCER_TOKEN')

class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_agency_test"
        self.database_path = "{}/{}".format(os.environ['DATABASE_URL'], database_name)
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()


    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_actors(self):
        res = self.client().get(
            '/actors',
            headers = {
                    "Authorization": "Bearer {}".format(executive_producer_token)
                })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))
        self.assertTrue(data['actors'])

    def test_add_actor(self):
        res = self.client().post(
            '/actors',
            headers = {
                "Authorization": "Bearer {}".format(executive_producer_token)
            },
            json = {
                'name': 'Ellen',
                'age': '25',
                'gender': 'female'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_actor(self):
        res = self.client().delete(
            '/actors/2',
            headers = {
                "Authorization": "Bearer {}".format(executive_producer_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])
    
    def test_edit_actor(self):
        res = self.client().patch(
            '/actors/3',
            headers = {
                "Authorization": "Bearer {}".format(executive_producer_token)
            },
            json = {
                'name': 'Michael',
                'age': '31',
                'gender': 'male'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_movies(self):
        res = self.client().get(
            '/movies',
            headers = {
                "Authorization": "Bearer {}".format(executive_producer_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))
        self.assertTrue(data['movies'])

    def test_add_movie(self):
        res = self.client().post(
            '/movies',
            headers = {
                "Authorization": "Bearer {}".format(executive_producer_token)
            },
            json = {
                'title': 'Moana',
                'release_date': '1.5.19'})
        data = json.loads(res.data)

    def test_delete_movie(self):
        res = self.client().delete(
            '/movies/3',
            headers = {
                "Authorization": "Bearer {}".format(executive_producer_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])

    def test_edit_movie(self):
        res = self.client().patch(
            '/movies/4',
            headers = {
                "Authorization": "Bearer {}".format(executive_producer_token)
            },
            json = {'title': 'Soul 3','release_date': '26.6.2025'})
        data = json.loads(res.data)
        print(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_if_delete_invalid_actor(self):
        res = self.client().delete(
            '/actors/1000',
            headers = {
                "Authorization": "Bearer {}".format(executive_producer_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'unprocessable')

    def test_422_if_delete_invalid_movie(self):
        res = self.client().delete(
            '/movies/1000',
            headers = {
                "Authorization": "Bearer {}".format(executive_producer_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'unprocessable')
    
    def test_422_if_edit_invalid_actor(self):
        res = self.client().patch(
            '/actors/1000',
            headers = {
                "Authorization": "Bearer {}".format(executive_producer_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'unprocessable')

    def test_422_if_edit_invalid_movie(self):
        res = self.client().patch(
            '/movies/1000',
            headers = {
                "Authorization": "Bearer {}".format(executive_producer_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'unprocessable')
    
    def test_422_if_add_actor_missing_details(self):
        res = self.client().post(
            '/actors',
            headers = {
                "Authorization": "Bearer {}".format(executive_producer_token)
            },
            json = {
                'name': 'Goldi',
                'gender': 'female'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'unprocessable')

    def test_422_if_add_movie_missing_details(self):
        res = self.client().post(
            '/movies',
            headers = {
                "Authorization": "Bearer {}".format(executive_producer_token)
            },
            json = {
                'title': 'Zootopia'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'unprocessable')

    def test_casting_assistant_get_actors_should_succeed(self):
        res = self.client().get(
            '/actors',
            headers = {
                "Authorization": "Bearer {}".format(casting_assistant_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_casting_assistant_delete_movie_should_fail(self):
        res = self.client().delete(
            '/movies/1',
            headers = {
                "Authorization": "Bearer {}".format(casting_assistant_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')

    def test_casting_director_add_actor_should_succeed(self):
        res = self.client().post(
            '/actors',
            headers = {
                "Authorization": "Bearer {}".format(casting_director_token)
            },
            json = {
                'name': 'Guy',
                'age': '45',
                'gender': 'male'
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_casting_director_delete_movie_should_fail(self):
        res = self.client().delete(
            '/movies/1',
            headers = {
                "Authorization": "Bearer {}".format(casting_director_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')

    def test_executive_producer_add_actor_should_succeed(self):
        res = self.client().post(
            '/actors',
            headers = {
                "Authorization": "Bearer {}".format(executive_producer_token)
            },
            json = {
                'name': 'Rachel',
                'age': '30',
                'gender': 'female'
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_executive_producer_delete_movie_should_succeed(self):
        res = self.client().delete(
            '/movies/1',
            headers = {
                "Authorization": "Bearer {}".format(executive_producer_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
   


if __name__ == "__main__":
    unittest.main()