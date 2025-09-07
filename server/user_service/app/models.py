from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6)

class UserInDB(BaseModel):
    id: Optional[str]
    email: EmailStr
    username: str
    hashed_password: str

class UserOut(BaseModel):
    id: Optional[str]
    email: EmailStr
    username: str
