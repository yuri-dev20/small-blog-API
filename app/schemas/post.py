from pydantic import BaseModel, ConfigDict
from typing import Optional

class PostBase(BaseModel):
    title: str
    text: str

    model_config = ConfigDict(from_attributes = True)

class PostOut(PostBase):
    id: int
    owner_id: int

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: Optional[str] = None
    text: Optional[str] = None

    model_config = ConfigDict(from_attributes = True)