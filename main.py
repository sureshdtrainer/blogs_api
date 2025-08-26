from fastapi import FastAPI
from pydantic import BaseModel


class Blog(BaseModel):
    id: int
    title: str
    content: str


app = FastAPI()


@app.post("/api/blogs")
def create_blog(blog: Blog):
    return blog


@app.get("/api/blogs")
def read_blogs():
    return "all blogs"


@app.get("/api/blogs/{id}")
def read_blog_id(id: int):
    return f"Blog {id}"


@app.put("/api/blogs/{id}")
def update_blog_id():
    pass


@app.delete("/api/blogs/{id}")
def delete_blog():
    pass
