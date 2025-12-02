from pydantic import BaseModel

class AIResponse(BaseModel):
    question: str | None
    text_response: str
    audio_base64: str
    is_correct: bool | None
    correct_answer: str | None
