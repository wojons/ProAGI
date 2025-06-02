import os
from typing import Generator

from sqlmodel import create_engine, Session, SQLModel

# Get database URL from environment variables
# The DATABASE_URL is expected to be set in the docker-compose.yml file
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # TODO: Log a critical error if DATABASE_URL is not set (Issue #XX)
    print("FATAL ERROR: DATABASE_URL environment variable not set.")
    # For POC, raise an error to stop execution
    raise EnvironmentError("DATABASE_URL environment variable not set.")

# Create the SQLAlchemy engine
# TODO: Configure connection pool size and other options for production (Issue #XX)
engine = create_engine(DATABASE_URL, echo=True) # echo=True for logging SQL statements (useful for debugging in POC)

def create_db_and_tables():
    """
    Creates the database tables based on SQLModel metadata.
    Use this function for initial setup or testing.
    """
    # TODO: Implement a proper database migration strategy (e.g., Alembic) for production (Issue #XX)
    print("Creating database tables...") # Basic logging
    SQLModel.metadata.create_all(engine)
    print("Database tables created.") # Basic logging

def get_session() -> Generator[Session, None, None]:
    """
    Dependency function to get a database session for FastAPI.
    Yields a session and closes it after the request is finished.
    """
    # TODO: Add error handling for database connection issues (Issue #XX)
    with Session(engine) as session:
        yield session

# Example usage (for testing database connection/creation if needed)
# if __name__ == "__main__":
#     # This block is for testing purposes only and should not run in production
#     print("Running database.py directly for testing...")
#     create_db_and_tables()
#     # TODO: Add more test logic here if needed (Issue #XX)
