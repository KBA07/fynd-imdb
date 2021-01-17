# fynd-imdb
An imdb API implementation, use user - admin, password - admin in basic auth for all POST, PUT and DELETE API calls.

    1. A GET API to get movies stored in the db
    Request:
    GET <host>/v1/movies?name=test&genre=Adventure&director=Vic&limit=100&offset=0
    :param name: optional
    :param genre: optional, should be exact
    :param director: optional
    :param limit: optional
    :param offset: optional
    
    Response:
    :return: 200, SUCCESS for a successful fetch
    200 response
    {
    "total": 2,
    "data": [
        {
            "id": 17,
            "99popularity": 82.0,
            "director": "Victor Fleming",
            "genre": [
                "Drama",
                "Romance",
                "War"
            ],
            "imdb_score": 8.2,
            "name": "Gone with the Wind"
        },
        {
            "id": 248,
            "99popularity": 99.0,
            "director": "Victo Fleming",
            "genre": [
                "Adventure",
                "Family",
                "Fantasy"
            ],
            "imdb_score": 8.3,
            "name": "test_input1"
        }
    ]
    }
    :return: 500, INTERNAL SERVER ERROR for issue on server side
    
    2. A POST API for adding new movies accepts json input. ALL Fields Mandatory
    POST <host>/v1/movies
        Request Body:
        {
        "99popularity": 83.0,
        "director": "Victor Fleming",
        "genre": [
          "Adventure",
          " Family",
          " Fantasy",
          " Musical"
        ],
        "imdb_score": 8.3,
        "name": "The Wizard of Oz"
        }
        Response:
        :return: 200, SUCCESS for a successful entry
        :return: 400, BAD REQUEST for issue in client request side
        :return: 401, UNAUTHORIZED for wrong user access
        :return: 500, INTERNAL SERVER ERROR for issue on server side
        
    3. A PUT API to edit existing movie details. Accepts id in param and all the edit fields in body.
        Request:
        PUT <host>/v1/movies?id=1
        :param id: Required
    
        Request Body: - Any one of the field given below is required
        {
        "99popularity": 83.0,
        "director": "Victor Fleming",
        "genre": [
          "Adventure",
          " Family",
          " Fantasy",
          " Musical"
        ],
        "imdb_score": 8.3,
        "name": "The Wizard of Oz"
        }
    
        Response:
        :return: 200, SUCCESS for a successful edition
        :return: 400, BAD REQUEST for issue in client request side
        :return: 401, UNAUTHORIZED for wrong user access
        :return: 500, INTERNAL SERVER ERROR for issue on server side
        
    4. A DELETE API to delete movies stored in db based on the id passed in param
        Request:
        DELETE v1/movies?id=1
        :param id: Required
    
        Response:
        :return: 200, SUCCESS for a successful deletion
        :return: 400, BAD REQUEST for issue in client request side
        :return: 401, UNAUTHORIZED for wrong user access
        :return: 500, INTERNAL SERVER ERROR for issue on server side
        