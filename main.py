import os
import uvicorn
from fastapi import FastAPI, Request, HTTPException, Body
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from typing import Union, Any
from utils.weather_requester import call_weather
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis

from dotenv import load_dotenv
load_dotenv()


from settings import settings


app = FastAPI(
    debug=True,
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@cache()
async def get_cache():
    return 1

@app.post("/weather")
@cache(expire=60)
def weather( payload: Any = Body(None)):
    try:
        city=payload["city"]
        param=payload["parameters"]
    except Exception as e:
        raise HTTPException(detail='Bad json',
                            status_code=status.HTTP_400_BAD_REQUEST)

    r = call_weather(payload["city"])
    if r.status_code != 200:
        if r.status_code == 404:
            raise HTTPException(detail='Can\'t find a city',
                            status_code=status.HTTP_404_NOT_FOUND)
        else:
            raise HTTPException(detail='Can\'t get answer from weather server',
                                status_code=status.HTTP_400_BAD_REQUEST)
    d=r.json()
    result={}
    result["weather"] = d["weather"][0]["main"]
    if "temperature" in param:
        result["temperature"] = d["main"]["temp"]
    if "feels" in param:
        result["feels"]=d["main"]['feels_like']
    if "wind" in param:
        result["wind"]=d["wind"]
    if "visibility" in param:
        result["visibility"]=d["visibility"]
    if "humidity" in param:
        result["humidity"]=d["main"]["humidity"]
    return result

@app.post("/many_weather")
@cache(expire=60)
def weather(payload: Any = Body(None)):
    try:
        cities = payload["cities"]
        param = payload["parameters"]
    except Exception as e:
        raise HTTPException(detail='Bad json',
                            status_code=status.HTTP_400_BAD_REQUEST)
    result = {}
    for city in cities:
        result[city]={}
        r = call_weather(city)
        if r.status_code != 200:
            result[city]=r.status_code
        else:
            d = r.json()
            result[city]["weather"] = d["weather"][0]["main"]
            if "temperature" in param:
                result[city]["temperature"] = d["main"]["temp"]
            if "feels" in param:
                result[city]["feels"] = d["main"]['feels_like']
            if "wind" in param:
                result[city]["wind"] = d["wind"]
            if "visibility" in param:
                result[city]["visibility"] = d["visibility"]
            if "humidity" in param:
                result[city]["humidity"] = d["main"]["humidity"]
    return result


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://redis", encoding="utf8", decode_responses=False)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

def run():
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)


if __name__ == '__main__':
    run()