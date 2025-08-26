
from sqlmodel import Session, SQLModel, create_engine

# sqlite_file_name = "blogs.db"
# sqlite_url = f"sqlite:///{sqlite_file_name}"

DATABASE_URL = "postgresql://postgres:admin@localhost:5432/blogsdb"

# connect_args = {"check_same_thread": True}
engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
