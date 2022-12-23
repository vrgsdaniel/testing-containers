from pydantic import BaseModel


class User(BaseModel):
    """Representation of User entity"""

    name: str
    email: str
