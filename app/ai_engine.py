from google import genai
import os, json, re
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
def get_text(response):
    # Case 1: response.text is a property (string)
    if isinstance(response.text, str):
        return response.text

    # Case 2: response.text is a function
    try:
        return response.text()
    except:
        pass

    # Case 3: extract from content parts
    if hasattr(response, "candidates"):
        parts = response.candidates[0].content.parts
        return "".join([p.text for p in parts if hasattr(p, "text")])

    raise ValueError("Unable to extract text from Gemini response")

async def generate_question():
    prompt = """
    Génère une question simple en français pour un élève niveau collège.
    Retourne uniquement un JSON strict :
    {"question": "...", "answer": "..."}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    raw = get_text(response)

    # Remove Markdown
    raw = re.sub(r"```json|```", "", raw).strip()

    return json.loads(raw)
async def correct_answer(question, correct_answer, student_answer):
    prompt = f"""
    Question : {question}
    Réponse correcte : {correct_answer}
    Réponse élève : {student_answer}

    Retourne uniquement un JSON :
    {{"correct": true/false, "feedback": "..."}}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    raw = get_text(response)
    raw = re.sub(r"```json|```", "", raw).strip()

    return json.loads(raw)


