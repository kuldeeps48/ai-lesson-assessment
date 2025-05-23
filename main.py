from typing import Annotated
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

from fastapi import UploadFile, FastAPI, Form, HTTPException
from fastapi.responses import StreamingResponse

from llm import check_question_answer, get_assessment_response
from ocr import extract_text


app = FastAPI()


@app.post("/generate-assessment")
async def upload_lesson_generate_assessment(file: UploadFile):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=415, detail="Unsupported file type. Only PDF files are allowed.")
    file_data = await file.read()
    try:
        _validate_file_size(file_data)
    except ValueError as e:
        raise HTTPException(status_code=413, detail=str(e))

    try:
        text = extract_text(file_data)
    except Exception:
        raise HTTPException(status_code=500, detail="Error during text extraction.")

    try:
        return StreamingResponse(get_assessment_response(lesson_text=text))
    except Exception:
        raise HTTPException(status_code=500, detail="Error during AI processing.")


@app.post("/check-answer")
async def check_answer(
    file: UploadFile,
    question_with_choices: Annotated[str, Form()],
    correct_answer: Annotated[str, Form()],
):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=415, detail="Unsupported file type. Only PDF files are allowed.")
    file_data = await file.read()
    try:
        _validate_file_size(file_data)
    except ValueError as e:
        raise HTTPException(status_code=413, detail=str(e))

    try:
        text = extract_text(file_data)
    except Exception:
        raise HTTPException(status_code=500, detail="Error during text extraction.")

    try:
        return StreamingResponse(
            check_question_answer(
                lesson_text=text,
                question_with_choices=question_with_choices,
                correct_answer=correct_answer,
            )
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Error during AI processing.")


def _validate_file_size(file_data: bytes):
    # Limit file size to 1MB
    if len(file_data) > 1_000_000:
        raise ValueError("File size exceeds 1MB limit.")
