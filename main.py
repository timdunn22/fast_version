from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
import requests
import json
app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/movies/_search")
async def movies(request: dict):
    the_response = requests.post('http://localhost:9200/_search/', data=json.dumps(request), 
                                          headers={'Content-Type': 'application/json'}).text
    # print(f'the response was {the_response}')
    # print('the response type is', type(the_response))
    # print(f'the response dumps type is  {type(json.dumps(the_response))}')
    # print(f'the response load type is  {type(json.load(the_response))}')
    # print(f'the response loads type is  {type(json.loads(the_response))}')
    return json.loads(the_response)

@app.get("/movies/_search")
async def movies(request: dict):
    the_response = requests.post('http://localhost:9200/_search/', data=json.dumps(request), 
                                          headers={'Content-Type': 'application/json'}).text
    return json.loads(the_response)

@app.get("/movies/{id}")
async def movies(id: int):
    data = {
        "query": {
            "ids" : {
                "values" : [id]
            }
        }
    }
    the_response = requests.post('http://localhost:9200/_search/', data=json.dumps(data), 
                                          headers={'Content-Type': 'application/json'}).text
    starting_response = json.loads(the_response).get('hits').get('hits')[0].get('_source')
    return starting_response

