# services/llm_service.py

from groq import Groq

from config import Config


client = Groq(
    api_key=Config.GROQ_API_KEY
)


def generate_response(
    system_prompt,
    user_prompt,
    temperature=0.2,
    max_tokens=1000
):

    response = client.chat.completions.create(
        model=Config.GROQ_MODEL,

        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],

        temperature=temperature,

        max_tokens=max_tokens
    )

    return response.choices[0].message.content