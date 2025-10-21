from sqlmodel import SQLModel, create_engine, Session

# SQLite database URL
DATABASE_URL = "sqlite:///./database.db"

# Create the SQLite engine
engine = create_engine(DATABASE_URL, echo=True)

# Dependency to get a session
def get_session():
    with Session(engine) as session:
        yield session

# Function to initialize the database
def init_db():
    SQLModel.metadata.create_all(engine)