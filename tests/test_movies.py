import os
import json
import base64

import unittest

from conf.settings import Config
from helpers.db import load_db
from helpers.response_maker import ResponseMaker
from webapp import create_app

app = create_app()


class TestMovies(unittest.TestCase):

    test_data = {
        "director": "Victor Fleming",
        "genre": [
            "Adventure",
            " Family",
            " Fantasy"
        ],
        "99popularity": 87,
        "imdb_score": 8.3,
        "name": "test_input1"
    }

    @classmethod
    def setUpClass(cls):
        load_db()

    def setUp(self):
        self.auth = base64.b64encode(b'admin:admin').decode()
        self.headers = {"Authorization": f"Basic {self.auth}"}
        self.API_URI = "v1/movies"

    def test_001_movies_post_api(self):
        data = TestMovies.test_data

        with app.test_client() as client:
            # Checking 401
            response = client.post(self.API_URI, data=json.dumps(data))
            self.assertEqual(ResponseMaker.RESPONSE_401, response.status_code)

            # Check response 200 with output Success case
            response = client.post(self.API_URI, data=json.dumps(data), headers=self.headers)
            self.assertEqual(ResponseMaker.RESPONSE_200, response.status_code)

            # Check response 400 with entry exists
            response = client.post(self.API_URI, data=json.dumps(data), headers=self.headers)
            self.assertEqual(ResponseMaker.RESPONSE_400, response.status_code)
            self.assertEqual(ResponseMaker.RESPONSE_400_ERROR_ENTRY_PRESENT,
                             json.loads(response.get_data(as_text=True)).get('err_code'))

            # Check response 400 for a missing field
            del data['99popularity']
            response = client.post(self.API_URI, data=json.dumps(data), headers=self.headers)
            self.assertEqual(ResponseMaker.RESPONSE_400, response.status_code)
            self.assertEqual(ResponseMaker.RESPONSE_400_ERROR_MISSING_FIELDS,
                             json.loads(response.get_data(as_text=True)).get('err_code'))

            # Check 99popularity and imdb score out of bounds
            data['99popularity'] = -1
            response = client.post(self.API_URI, data=json.dumps(data), headers=self.headers)
            self.assertEqual(ResponseMaker.RESPONSE_400, response.status_code)
            self.assertEqual(ResponseMaker.RESPONSE_400_ERROR_OUT_OF_BOUNDS,
                             json.loads(response.get_data(as_text=True)).get('err_code'))

            data['99popularity'] = 101
            response = client.post(self.API_URI, data=json.dumps(data), headers=self.headers)
            self.assertEqual(ResponseMaker.RESPONSE_400, response.status_code)
            self.assertEqual(ResponseMaker.RESPONSE_400_ERROR_OUT_OF_BOUNDS,
                             json.loads(response.get_data(as_text=True)).get('err_code'))

            data['99popularity'] = 87
            data['imdb_score'] = -1
            response = client.post(self.API_URI, data=json.dumps(data), headers=self.headers)
            self.assertEqual(ResponseMaker.RESPONSE_400, response.status_code)
            self.assertEqual(ResponseMaker.RESPONSE_400_ERROR_OUT_OF_BOUNDS,
                             json.loads(response.get_data(as_text=True)).get('err_code'))

            data['imdb_score'] = 11
            response = client.post(self.API_URI, data=json.dumps(data), headers=self.headers)
            self.assertEqual(ResponseMaker.RESPONSE_400, response.status_code)
            self.assertEqual(ResponseMaker.RESPONSE_400_ERROR_OUT_OF_BOUNDS,
                             json.loads(response.get_data(as_text=True)).get('err_code'))

    def test_002_movies_delete_api(self):
        data = TestMovies.test_data

        with app.test_client() as client:
            # Adding entry
            client.post(self.API_URI, data=json.dumps(data), headers=self.headers)

            # Getting added entry
            response = client.get(self.API_URI, query_string={'name': data['name']})
            content = json.loads(response.get_data(as_text=True)).get('data')[0]
            print(content)
            self.assertTrue(content)

            # Checking 401
            response = client.delete(self.API_URI, query_string={'id': content.get('id')})
            self.assertEqual(ResponseMaker.RESPONSE_401, response.status_code)

            # Checking 400
            response = client.delete(self.API_URI, headers=self.headers)
            self.assertEqual(ResponseMaker.RESPONSE_400, response.status_code)
            self.assertEqual(ResponseMaker.RESPONSE_400_ERROR_MISSING_FIELDS,
                             json.loads(response.get_data(as_text=True)).get('err_code'))

            # Deleting entry to check 200
            response = client.delete(self.API_URI, query_string={'id': content.get('id')},
                                     headers=self.headers)
            self.assertEqual(ResponseMaker.RESPONSE_200, response.status_code)

            # Getting after deleted entry
            response = client.get(self.API_URI, query_string={'name': data['name']})
            content = json.loads(response.get_data(as_text=True)).get('data')
            self.assertFalse(content)

    @classmethod
    def tearDownClass(cls):
        working_dir = os.getcwd()
        os.remove(working_dir + f'/{Config.SQLITEDB}')
