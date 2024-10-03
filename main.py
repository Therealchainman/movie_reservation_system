# main.py
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import database

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "API for Movie Reservation System"}

@app.get("/movies/")
async def read_movies() -> List[database.Movie]:
    conn = await database.startup()
    try:
        movies = await database.select_movies(conn)
        return movies
    finally:
        await database.shutdown(conn)

@app.post("/movies/")
async def create_movie(movie: database.Movie) -> dict:
    conn = await database.startup()
    try:
        inserted_movie = await database.insert_movie(movie.name, movie.genre, movie.runtime, conn)
        return {"message": "Movie inserted", "movie": inserted_movie}
    finally:
        await database.shutdown(conn)

# @app.get("/items/{item_id}")
# async def read_item(item: Item):
#     return item.name

# @app.post("/items/")
# async def create_item(item: Item):
#     return item