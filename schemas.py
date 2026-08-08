from pydantic import BaseModel


class Query(BaseModel):
    message: str


class AskResponse(BaseModel):
    question: str
    answer: str