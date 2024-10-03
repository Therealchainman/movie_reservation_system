from typing import List
import asyncpg
from pydantic import BaseModel

class Movie(BaseModel):
    name: str
    genre: str
    runtime: int

async def startup():
    conn = await asyncpg.connect(
        user = "admin",
        password = "123456",
        database = "default",
        host = "127.0.0.1", # localhost
        port = 5432
    )
    # Check the connection by running a simple query
    result = await conn.fetchval("SELECT 1")
    if result == 1:
        print("Connection successful!")
    return conn
async def shutdown(conn):
    await conn.close()
    if conn.is_closed():
        print("The connection is closed.")
    else:
        print("The connection is still open.")
async def list_tables(conn):
    query = """
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'public';
    """
    tables = await conn.fetch(query)
    print(tables)
    for table in tables:
        print(table["table_name"])
# create a table
async def create_movies_table(conn):
    # TODO: genre should be a list of genres
    query = """
    CREATE TABLE IF NOT EXISTS movies (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        genre VARCHAR(255),
        runtime INTEGER NOT NULL,
        UNIQUE (name)
    );
    CREATE INDEX IF NOT EXISTS idx_movie_name ON movies (name);
    """
    await conn.execute(query)
    print("Table created.")
# insert movie into the table
async def insert_movie(name, genre, runtime, conn):
    query = f"""
    INSERT INTO movies (name, genre, runtime)
    VALUES ($1, $2, $3)
    RETURNING *;
    """
    record = await conn.fetchrow(query, name, genre, runtime)
    return Movie(**record)
# delete a movie from the table
async def delete_movie(name, conn):
    query = """
    DELETE FROM movies
    WHERE name = $1;
    """
    await conn.execute(query, name)
    print("Movie deleted.")
# update a movie in the table
async def update_movie(name, genre, runtime, conn):
    query = """
    UPDATE movies
    SET genre = $2, runtime = $3
    WHERE name = $1;
    """
    await conn.execute(query, name, genre, runtime)
    print("Movie updated.")
# select all movies from the table
async def select_movies(conn) -> List[Movie]:
    query = """
    SELECT * FROM movies;
    """
    records = await conn.fetch(query)
    movies = [Movie(**record) for record in records]
    return movies
# clear the movies table
async def clear_movies_table(conn):
    query = """
    DELETE FROM movies;
    """
    await conn.execute(query)
    print("Table cleared.")
async def delete_movies_table(conn):
    query = """
    DROP TABLE IF EXISTS movies;
    DROP INDEX IF EXISTS idx_movie_name;
    """
    await conn.execute(query)
    print("Table deleted.")