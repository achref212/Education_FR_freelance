import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")   # FREE TIER MODEL

async def generate_question():
    prompt = """
    Génère une question simple en français pour un élève niveau collège.
    Domaine : grammaire, conjugaison ou vocabulaire.
    Retourne sous ce format JSON sans texte supplémentaire :
    {"question": "...", "answer": "..."}
    """

    response = model.generate_content(prompt)
    text = response.text.strip()
    return eval(text)

async def correct_answer(question, correct_answer, student_answer):
    prompt = f"""
    Question : {question}
    Réponse correcte : {correct_answer}
    Réponse élève : {student_answer}

    Analyse la réponse de l'élève.
    Répond seulement en JSON :
    {{"correct": true/false, "feedback": "..."}}    
    """

    response = model.generate_content(prompt)
    text = response.text.strip()
    return eval(text)
