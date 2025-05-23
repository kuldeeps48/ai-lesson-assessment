# AI Lesson Assessment

This application processes educational materials (lessons, notes) to generate assessments (Multiple Choice Questions) for students. It utilizes Optical Character Recognition (OCR) to extract text from uploaded PDF documents, including specialized extraction for mathematical expressions, and then employs a Large Language Model (LLM) to create relevant questions.

## Features

*   **PDF Text Extraction**: Extracts text from uploaded PDF files using OCR (Tesseract).
*   **Mathematical Expression Extraction**: Identifies and extracts LaTeX-like mathematical expressions from PDFs using `pix2tex` (via `pix2tex.cli.LatexOCR`). These expressions are appended to the main text under the heading "Maths expressions:" and are utilized by the LLM for generating questions and checking answers.
*   **Multilingual Support**: Supports text extraction and assessment generation for English, Hindi, and Devanagari scripts (as supported by Tesseract OCR).
*   **Assessment Generation**: Generates multiple-choice questions based on the extracted lesson content using an LLM.
*   **Answer Checking**: Allows users to submit answers to generated questions and receive feedback, also powered by the LLM.
*   **Configuration Management**: Uses Pydantic for managing settings via environment variables (e.g., API keys, LLM parameters).
*   **File Validation**:
    *   Strictly enforces PDF file uploads (`application/pdf`). Non-PDF files result in an HTTP 415 error.
    *   Limits file size to 1MB. Oversized files result in an HTTP 413 error.

## Setup and Installation

1.  **Create `.env` File**:
    Copy the `.env.example` file to a new file named `.env`. Update this file with your `OPENAI_API_KEY` and any other desired LLM configuration values (see `config.py` for available settings).
    ```bash
    cp .env.example .env
    # Now, edit .env with your API key and other settings
    ```

2.  **Create Virtual Environment and Install Dependencies**:
    It is recommended to use a virtual environment for managing project dependencies.
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
    ```
    Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```
    The dependencies include libraries such as FastAPI, Pytesseract for OCR, `pix2tex[cli]` for math extraction (which in turn uses `torch` and `torchvision`), Langchain for LLM interaction, and Pydantic for settings management. The `pix2tex` model checkpoints are typically downloaded automatically on first use if not already present.

## Running the Application

You can run the application using Uvicorn, which is an ASGI server suitable for FastAPI:

```bash
uvicorn main:app --reload --port 8080
```
This will start the server, usually accessible at `http://localhost:8080`. The `--reload` flag enables automatic reloading of the server when code changes are detected, which is useful for development.

### Docker
Alternatively, you can build and run the application using Docker:

1.  **Build the Docker image**:
    ```bash
    docker build -t ai-lesson-assessment .
    ```
2.  **Run the Docker container**:
    Make sure your `.env` file is correctly populated with your `OPENAI_API_KEY`.
    ```bash
    docker run -it -p 8080:8080 --env-file .env ai-lesson-assessment
    ```
    The `--env-file .env` flag passes the environment variables from your `.env` file to the container.

To deactivate the virtual environment (if you used one without Docker):
```bash
deactivate
```

The application exposes the following API endpoints:

**Important Note on File Uploads**: Both endpoints strictly require PDF files (`application/pdf`). Uploading any other file type will result in an HTTP 415 (Unsupported Media Type) error. The maximum allowed file size is 1MB; larger files will result in an HTTP 413 (Payload Too Large) error. (File size validation was added in a previous task, but good to mention here for completeness).

## `/generate-assessment`
Generates multiple-choice questions from the provided PDF lesson file.

### Request
```bash
curl --location 'http://localhost:8080/generate-assessment' \
--header 'accept: application/json' \
--form 'file=@"/path/to/your/lesson.pdf"'
```

### Response
A streaming response containing the generated questions.

## `/check-answer`
Checks a user-provided answer against the lesson content and a specific question.

### Request
```bash
curl --location 'http://localhost:8080/check-answer' \
--form 'file=@"/path/to/your/lesson.pdf"' \
--form 'question_with_choices="<Your Question Here, Including Choices>"' \
--form 'correct_answer="<The Correct Answer String>"'
```
**Example `question_with_choices`**: `"What percentage of the Solar System's total mass does the Sun account for?\nA) 50%\nB) 75%\nC) 95%\nD) 99.8%"`

**Example `correct_answer`**: `"D) 99.8%"` (or just `"99.8%"`, ensure consistency with how questions are generated/expected)

### Response
A streaming response containing feedback on the answer (e.g., "Correct" or "Incorrect" with explanation).
