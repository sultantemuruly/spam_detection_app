from pydantic import BaseModel


class EmailSchema(BaseModel):
    text: str
