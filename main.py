from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
import requests
import json
app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8001",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def post_return_search_results(request):
    the_response = requests.post('http://localhost:9200/_search/', data=json.dumps(request), 
                                 headers={'Content-Type': 'application/json'}).text
    return json.loads(the_response)

def get_one_search_result(request):
    the_response = post_return_search_results(request)
    return the_response.get('hits').get('hits')[0].get('_source')

def get_many_search_results(request):
    the_response = post_return_search_results(request)
    return the_response.get('hits').get('hits')

@app.post("/movies/_search")
async def movies(request: dict):
    return post_return_search_results(request)

@app.get("/movies/_search")
async def movies(request: dict):
    return post_return_search_results(request)

@app.get("/movies/{id}")
async def movies(id: int):
    data = {
        "query": {
            "ids" : {
                "values" : [id]
            }
        }
    }
    return get_one_search_result(data)


@app.get("/movies/top_imdb")
async def movies():
    data = {
        "query": {
            "range" : {
                "top_250_rank" : {
                    "gte" : 1
                }
            }
        }
    }
    return get_many_search_results(data)

@app.get("/movies/trending")
async def movies():
    # data = {
    #     "query": {
    #         "range" : {
    #             "top_popular_rank" : {
    #                 "gte" : 1
    #             }
    #         }
    #     }
    # }
    # return get_many_search_results(data)
    return {"whatever": "cool"}


@app.get("/something")
async def something():
    return {"whatever": "yes"}

@app.get("/movies/genre/{genre}")
async def movies(genre: str):
    data = {
        "query": {
        "bool": {
            "must": [{"term": {"genre_ranking.genre": genre}}, {"range": {"genre_ranking.ranking": {"gte": 1}}}]
        }
        }
    }
    return get_many_search_results(data)

