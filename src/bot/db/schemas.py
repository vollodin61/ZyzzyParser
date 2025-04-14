from pydantic import BaseModel


class BaseSchema(BaseModel):
    class Config:
        from_attributes = True


class DataFromTablesSchema(BaseSchema):
    title: str
    url: str
    xpath: str
