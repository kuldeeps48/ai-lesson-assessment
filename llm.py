import os

if not os.environ.get("OPENAI_API_KEY"):
    raise ValueError("API key for OpenAI is not set")

from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

model = init_chat_model(
    model="gpt-4o-mini",
    max_tokens=10000,
    temperature=0.1,
)


async def get_assessment_response(lesson_text: str):
    print("Using LLM")
    try:
        system_template = "Generate 3 multiple choice questions based on the following lesson text. Each question should have 4 options. Questions should be based on the content of the lesson text. Choices should be plausible and not easily guessable. Only one choice should be the correct answer. Keep the questions simple and straightforward. Keep choices clear and concise. Avoid using negative questions. Avoid using 'all of the above' or 'none of the above' as choices. If the lesson has maths expressions, they might be included in the lesson after text 'Maths expressions:'. Check for validity of maths expressions and use them only if they are valid. Lesson can be in 3 languages: English, Hindi, and Devanagari. If the lesson is in Hindi or Devanagari, the questions should be in the same language. If the lesson is in English, the questions should be in English. Reverify the questions to ensure they are correct and make sense."

        prompt_template = ChatPromptTemplate.from_messages(
            [("system", system_template), ("user", lesson_text)]
        )
        for chunk in model.stream(prompt_template.format_messages()):
            if chunk:
                yield f"{chunk.content}"
    except Exception as e:
        print(e)
        yield f"Error: {e}"


async def check_question_answer(
    lesson_text: str, question_with_choices: str, correct_answer: str
):
    print("Using LLM")
    try:
        system_template = "Check if the answer to the following question is correct based on the lesson text. Provide feedback on the answer. If the answer is incorrect, provide the correct answer and the relevant part of the lesson text that supports the correct answer. If the answer is correct, say 'Correct' and nothing else. If the answer is incorrect, say 'Incorrect' followed by the correct answer and the relevant part of the lesson text that supports the correct answer. Do not make the feedback too long. Keep it concise and to the point. Do not make up the correct answer. Provide the correct answer based on the lesson text.  If the lesson has maths expressions, they might be included in the lesson after text 'Maths expressions:'. Check for validity of maths expressions and use them only if they are valid. Lesson can be in 3 languages: English, Hindi, and Devanagari. If the lesson is in Hindi or Devanagari, the questions should be in the same language. If the lesson is in English, the questions should be in English. Re-verify the questions to ensure they are correct and make sense. Lesson text: {lesson_text}"
        prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", system_template),
                (
                    "user",
                    "Question with choices: {question_with_choices} \n\n Correct answer: {correct_answer}",
                ),
            ]
        )

        for chunk in model.stream(
            prompt_template.format_messages(
                lesson_text=lesson_text,
                question_with_choices=question_with_choices,
                correct_answer=correct_answer,
            )
        ):
            if chunk:
                yield f"{chunk.content}"
    except Exception as e:
        print(e)
        yield f"Error: {e}"
