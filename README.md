# ai-lesson-assessment

Take lessons, notes as input. Perform OCR and generate an assessment (MCQs) on the fly for students.

Create a .env file based on the .env.example file.

Then, create a virtual environment and install the dependencies.

```bash
python -m venv .venv

source .venv/bin/activate
```

To install the dependencies, run the following command:

```bash
pip install -r requirements.txt
```

Build and run the docker image

```bash
docker build -t ai-lesson-assessment .
docker run -it -p 8080:8080 ai-lesson-assessment
```

To deactivate the virtual environment, run the following command:

```bash
deactivate
```

# APIs

```
curl --location 'http://localhost:8080/generate-assessment' \
--header 'accept: application/json' \
--form 'file=@"/Users/kuldeepsingh/Downloads/lesson.pdf"'
```

```
curl --location 'http://localhost:8080/check-answer' \
--form 'file=@"/Users/kuldeepsingh/Downloads/lesson.pdf"' \
--form 'question_with_choices="What percentage of the Solar System'\''s total mass does the Sun account for?
A) 50%
B) 75%
C) 95%
D) 99.8% "' \
--form 'correct_answer="99.8%"'
```
