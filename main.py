from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select


class BlogBase(SQLModel):  # Base Model
    title: str = Field(max_length=100)
    content: str = Field(max_length=1000)


class Blog(BlogBase, table=True):  # DB Access
    id: int | None = Field(default=None, primary_key=True)


class BlogCreate(BlogBase):  # Create
    pass


class BlogPublic(BlogBase):  # Response for create and read
    id: int


class BlogUpdate(SQLModel):
    title: str | None
    content: str | None


sqlite_file_name = "blogs.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/api/blogs", response_model=BlogPublic, status_code=status.HTTP_201_CREATED)
def create_blog(blog: BlogCreate):
    with Session(engine) as session:
        db_blog = Blog.model_validate(blog)
        session.add(blog)
        session.commit()
        session.refresh(blog)
        return blog


@app.get("/api/blogs", response_model=list[BlogPublic])
def read_blogs():
    with Session(engine) as session:
        blogs = session.exec(select(Blog)).all()
        return blogs


@app.get("/api/blogs/{id}", response_model=BlogPublic)
def read_blog_id(id: int):
    with Session(engine) as session:
        blog = session.get(Blog, id)
        if not blog:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
        return blog


@app.put("/api/blogs/{id}", response_model=BlogPublic)
def update_blog_id(blog_id: int, blog: BlogUpdate):
    with Session(engine) as session:
        db_blog = session.get(Blog, id)
        if not blog:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
        # get the value from above update obj and create a DB object
        blog_updated_data = blog.model_dump(exclude_unset=True)
        db_blog.sqlmodel_update(blog_updated_data)
        session.add(db_blog)
        session.commit()
        session.refresh(db_blog)
        return db_blog


@app.delete("/api/blogs/{id}")
def delete_blog(id: int):
    with Session(engine) as session:
        db_blog = session.get(Blog, id)
        if not db_blog:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
        session.delete(db_blog)
        session.commit()
        return {"detail": "Blog deleted"}
