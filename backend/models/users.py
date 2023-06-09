from enum import Enum
from bson import ObjectId
from pydantic import EmailStr, Field, BaseModel, validator
from typing import Optional
from email_validator import validate_email, EmailNotValidError
from models.base import MongoBaseModel

class Role(str, Enum):
    SALESMAN = "SALESMAN"
    ADMIN = "ADMIN"

class UserBase(MongoBaseModel):
    username: str = Field(..., min_length=3, max_length=15)
    email: str = Field(...)
    password: str = Field(...)
    role: Role

    @validator("email")
    def valid_email(cls, v):
        try:
            email = validate_email(v).email
            return email
        except EmailNotValidError as e:
            raise EmailNotValidError
    
class LoginBase(BaseModel):
  email: str = EmailStr(...)
  password: str = Field(...)

class CurrentUser(BaseModel):
  email: str = EmailStr(...)
  password: str = Field(...)
  role: str = Field(...)
