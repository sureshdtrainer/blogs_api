
from fastapi import HTTPException, status
from sqlmodel import select

from models.schemas import Blog


def create_blog(session, blog):
    db_blog = Blog.model_validate(blog)
    session.add(db_blog)
    session.commit()
    session.refresh(db_blog)
    return db_blog


def read_blogs(session):
    blogs = session.exec(select(Blog)).all()
    return blogs


def read_blog_id(session, id):
    blog = session.get(Blog, id)
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    return blog


def update_blog_id(session, id, blog):
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


def delete_blog(session, id):
    db_blog = session.get(Blog, id)
    if not db_blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    session.delete(db_blog)
    session.commit()
    return {"detail": "Blog deleted"}
