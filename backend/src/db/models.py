from typing import Optional
from sqlmodel import Field, SQLModel

# Define a simple model for storing API keys
class ApiKey(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    app_id: str = Field(index=True)
    hashed_key: str
    user_id: Optional[str] = Field(default=None, index=True)
    permissions: str # Store as comma-separated string for simplicity in POC
    is_active: bool = Field(default=True)

    # TODO: Add created_at and updated_at timestamps (Issue #XX)
    # TODO: Consider a more structured way to store permissions (e.g., JSON field if supported by DB and ORM) (Issue #XX)
    # TODO: Add relationship to User model if user management is implemented (Issue #XX)

    # TODO: Add other database models as needed (e.g., AppConfig, etc.) (Issue #XX)

# Define a model for users
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(unique=True, index=True) # Unique identifier for the user
    username: str = Field(unique=True, index=True)
    hashed_password: str
    email: Optional[str] = Field(default=None, index=True)
    is_active: bool = Field(default=True)
    roles: str = Field(default="") # Store as comma-separated string for simplicity in POC
    created_at: Optional[str] = Field(default=None) # ISO 8601 timestamp
    updated_at: Optional[str] = Field(default=None) # ISO 8601 timestamp

    # TODO: Add relationships to other models (e.g., ApiKey) (Issue #XX)
