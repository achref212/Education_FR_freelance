from fastapi import FastAPI, UploadFile
from app.ai_engine import generate_question, correct_answer
from app.voice import speech_to_text, text_to_audio_base64
from app.models import AIResponse

app = FastAPI(title="Free Gemini 2.5 Chatbot Educatif")

current_question = None

@app.get("/question", response_model=AIResponse)
async def ask_question():
    global current_question
    current_question = await generate_question()

    audio = text_to_audio_base64(current_question["question"])

    return AIResponse(
        question=current_question["question"],
        text_response=current_question["question"],
        audio_base64=audio,
        is_correct=None,
        correct_answer=None
    )

@app.post("/answer", response_model=AIResponse)
async def answer_student(file: UploadFile):
    global current_question

    student_text = speech_to_text(file.file)

    result = await correct_answer(
        question=current_question["question"],
        correct_answer=current_question["answer"],
        student_answer=student_text
    )

    reply_text = (
        "Très bien, ta réponse est correcte !" if result["correct"]
        else f"Ce n'est pas correct. La bonne réponse est : {current_question['answer']}"
    )

    audio = text_to_audio_base64(reply_text)

    return AIResponse(
        question=None,
        text_response=reply_text,
        audio_base64=audio,
        is_correct=result["correct"],
        correct_answer=current_question["answer"]
    )
