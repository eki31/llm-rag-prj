from pydantic import BaseModel

class QuestionRequest(BaseModel):
    question: str

class SummarizeRequest(BaseModel):
    text: str