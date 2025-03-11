from typing import Annotated
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

from fastapi import UploadFile, FastAPI, Form
from fastapi.responses import StreamingResponse

from llm import check_question_answer, get_assessment_response
from ocr import extract_text


app = FastAPI()


@app.post("/generate-assessment")
async def upload_lesson_generate_assessment(file: UploadFile):
    file_data = await file.read()
    text = extract_text(file_data)

    return StreamingResponse(get_assessment_response(lesson_text=text))


@app.post("/check-answer")
async def check_answer(
    file: UploadFile,
    question_with_choices: Annotated[str, Form()],
    correct_answer: Annotated[str, Form()],
) -> str:
    file_data = await file.read()
    text = extract_text(file_data)
    return StreamingResponse(
        check_question_answer(
            lesson_text=text,
            question_with_choices=question_with_choices,
            correct_answer=correct_answer,
        )
    )
