from pydantic import BaseModel, ConfigDict
from typing import Optional

class PostBase(BaseModel):
    title: str
    text: str
    owner_id: int

    model_config = ConfigDict(from_attributes = True)

class PostOut(PostBase):
    id: int

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: Optional[str] = None
    text: Optional[str] = None
    owner_id: Optional[int] = None

    model_config = ConfigDict(from_attributes = True)