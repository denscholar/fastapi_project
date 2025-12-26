from fastapi import FastAPI, Response, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()


class PostModel(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


# database connection
while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fast_apiDB",
            user="postgres",
            password="sunshine",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("database connection was successful")
        break

    except Exception as e:
        print("problem connecting to the database. Reason:", {e})
        time.sleep(2)


class UpdatePost(BaseModel):
    title: str
    content: str
    rating: Optional[int] = None
    published: bool = True


# PATH OPERATION


# GET ALL POST
@app.get("/")
async def get_root():
    cursor.execute(""" SELECT * FROM post """)
    posts = cursor.fetchall()
    return {"data": posts}


# @app.get("/posts")
# async def get_posts() -> dict:
#     return {
#         "message": my_posts,
#     }


# CREATE A POST
@app.post("/posts", status_code=201)
async def create_post(post: PostModel) -> dict:
    cursor.execute(
        """ INSERT INTO post (title, content, published) VALUES(%s, %s, %s) RETURNING * """,
        (
            post.title,
            post.content,
            post.published,
        ),
    )
    new_post = cursor.fetchone()
    conn.commit()

    return {"message": "post succeeefully created", "data": new_post}


# GET A SINGLE POST
@app.get("/posts/{id}", status_code=status.HTTP_200_OK)
async def get_post(id: str) -> dict:
    cursor.execute("""SELECT * from post WHERE id = %s """, (id))
    post = cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(
            status_code=404, detail=f"post with id: {str(id),} was not found"
        )
    return {"message": "post found", "data": post}


# UPDATE POST
@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
async def update_post(id: str, updated_post: UpdatePost) -> dict:
    cursor.execute(
        """ UPDATE post SET title = %s, content=%s, published = %s WHERE id = %s RETURNING *""",
        (
            updated_post.title,
            updated_post.content,
            updated_post.published,
            str(id)
        ),
    )
    updated_post = cursor.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(status_code=404, detail=f"post with id: {id} was not found")

    return Response(
        content="Posts updated successfully", status_code=status.HTTP_200_OK
    )


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int) -> Response:
    cursor.execute(""" DELETE FROM post WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if not deleted_post:
        raise HTTPException(status_code=404, detail=f"post with id: {id} was not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
