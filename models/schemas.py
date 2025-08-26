from sqlmodel import Field, Session, SQLModel


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
