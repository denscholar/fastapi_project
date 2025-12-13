from fastapi import FastAPI, Response, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from random import randrange


app = FastAPI()


class PostModel(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


class UpdatePost(BaseModel):
    title: str
    content: str
    rating: Optional[int] = None


my_posts = [
    {
        "id": 1,
        "title": "First Post",
        "content": "This is my first post",
        "published": True,
        "rating": 5,
    },
    {
        "id": 2,
        "title": "Second Post",
        "content": "This is my second post",
        "published": False,
        "rating": None,
    },
]


# PATH OPERATION
@app.get("/")
async def get_root():
    return {"message": "Welcome to my API"}


@app.get("/posts")
async def get_posts() -> dict:
    return {
        "message": my_posts,
    }


@app.post("/posts", status_code=201)
async def create_post(post: PostModel) -> dict:
    new_post = post.model_dump()
    new_post["id"] = randrange(0, 1000000)
    my_posts.append(new_post)
    return {"message": "post succeeefully created", "data": new_post}


@app.get("/posts/{id}", status_code=status.HTTP_200_OK)
async def get_post(id: int) -> dict:
    for post in my_posts:
        if post["id"] == id:
            return {"message": "post found", "data": post}
    raise HTTPException(status_code=404, detail=f"post with id: {id} was not found")


@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
async def update_post(id: int, updated_post: UpdatePost) -> dict:
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            my_posts[index] = updated_post.model_dump()
            my_posts[index]["id"] = id
            return Response(
                content=f'{{"message": "post updated successfully", "data": {my_posts[index]}}}'
            )
        raise HTTPException(status_code=404, detail=f"post with id: {id} was not found")


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int) -> Response:
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            my_posts.pop(index)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"post with id: {id} was not found")
