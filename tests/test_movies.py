import json
import base64

import unittest
from webapp import create_app

app = create_app()


class TestMovies(unittest.TestCase):

    def setUp(self):
        self.auth = base64.b64encode(b'admin:admin').decode()

    def test_001_movies_post_api(self):

        with app.test_client() as client:
            data = {
                "director": "Victor Fleming",
                "genre": [
                    "Adventure",
                    " Family",
                    " Fantasy"
                ],
                "99popularity": 0,
                "imdb_score": 8.3,
                "name": "test_input1"
            }
            response = client.post('v1/movies', data=json.dumps(data),
                                   headers={"Authorization": f"Basic {self.auth}"})
            self.assertEqual(400, response.status_code)
