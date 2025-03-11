import os
from huggingface_hub import InferenceClient


print("HUGGINGFACEHUB_API_TOKEN: ", os.getenv("HUGGINGFACEHUB_API_TOKEN"))
client = InferenceClient(
    provider="together", api_key=os.getenv("HUGGINGFACEHUB_API_TOKEN")
)


async def get_assessment_response(lesson_text: str):
    try:
        print("Starting LLM")
        system_message = "Generate 3 multiple choice questions based on the following lesson text. Each question should have 4 options. Questions should be based on the content of the lesson text. Choices should be plausible and not easily guessable. Only one choice should be the correct answer. Keep the questions simple and straightforward. Keep choices clear and concise. Avoid using negative questions. Avoid using 'all of the above' or 'none of the above' as choices."

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": lesson_text},
        ]
        stream = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-R1",
            messages=messages,
            max_tokens=10000,
            stream=True,
        )
        for chunk in stream:
            t = chunk.choices[0].delta.content
            if t:
                yield f"{t}"
    except Exception as e:
        print(e)
        yield f"Error: {e}"


async def check_question_answer(
    lesson_text: str, question_with_choices: str, correct_answer: str
):
    try:
        print("Starting LLM")
        system_message = f"Check if the answer to the following question is correct based on the lesson text. Provide feedback on the answer. If the answer is incorrect, provide the correct answer and the relevant part of the lesson text that supports the correct answer. If the answer is correct, say 'Correct' and nothing else. If the answer is incorrect, say 'Incorrect' followed by the correct answer and the relevant part of the lesson text that supports the correct answer. Do not make the feedback too long. Keep it concise and to the point. Do not make up the correct answer. Provide the correct answer based on the lesson text. Lesson text: {lesson_text}"

        messages = [
            {"role": "system", "content": system_message},
            {
                "role": "user",
                "content": f"Question with choices: {question_with_choices} \n\n Correct answer: {correct_answer}",
            },
        ]
        stream = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-R1",
            messages=messages,
            max_tokens=10000,
            stream=True,
        )
        for chunk in stream:
            t = chunk.choices[0].delta.content
            if t:
                yield f"{t}"
    except Exception as e:
        print(e)
        yield f"Error: {e}"
