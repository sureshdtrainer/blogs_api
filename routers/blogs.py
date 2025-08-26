from fastapi import Depends, APIRouter, status
from sqlmodel import Field, Session
from db.database import get_session
from models.schemas import BlogCreate, BlogPublic, BlogUpdate
from repositories import blogs as repositories

router = APIRouter()


@router.post("/api/blogs", response_model=BlogPublic, status_code=status.HTTP_201_CREATED)
def create_blog(*, session: Session = Depends(get_session), blog: BlogCreate):
    return repositories.create_blog(session, blog)


@router.get("/api/blogs", response_model=list[BlogPublic])
def read_blogs(*, session: Session = Depends(get_session)):
    return repositories.read_blogs(session)


@router.get("/api/blogs/{id}", response_model=BlogPublic)
def read_blog_id(*, session: Session = Depends(get_session), id: int):
    return repositories.read_blog_id(session, id)


@router.put("/api/blogs/{id}", response_model=BlogPublic)
def update_blog_id(*, session: Session = Depends(get_session), id: int, blog: BlogUpdate):
    return repositories.update_blog_id(session, id, blog)


@router.delete("/api/blogs/{id}")
def delete_blog(*, session: Session = Depends(get_session), id: int):
    return repositories.delete_blog(session, id)
