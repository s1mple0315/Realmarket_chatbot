from pydantic import BaseModel


class Role(BaseModel):
    name: str
    description: Optional[str] = None

    class Config:
        orm_mode = True
