from groq import Groq

from config import Config


# ==========================================
# GROQ CLIENT
# ==========================================

client = Groq(
    api_key=Config.GROQ_API_KEY
)


# ==========================================
# WEB SEARCH
# ==========================================

def web_search(
    question,
    memory=""
):

    # --------------------------------------
    # Limit conversation memory
    # --------------------------------------

    if memory is None:
        memory = ""

    memory = str(memory)

    MAX_MEMORY_CHARS = 4000

    if len(memory) > MAX_MEMORY_CHARS:

        memory = memory[
            -MAX_MEMORY_CHARS:
        ]


    # --------------------------------------
    # Limit question size
    # --------------------------------------

    question = str(question)

    MAX_QUESTION_CHARS = 2000

    if len(question) > MAX_QUESTION_CHARS:

        question = question[
            :MAX_QUESTION_CHARS
        ]


    # --------------------------------------
    # Build compact prompt
    # --------------------------------------

    prompt = f"""
CONVERSATION MEMORY:
{memory}

CURRENT QUESTION:
{question}

Use current web information when required.

Provide a concise, reliable answer.

Clearly distinguish current information
from historical information.
"""


    # --------------------------------------
    # Groq Compound request
    # --------------------------------------

    response = client.chat.completions.create(

        model=Config.GROQ_WEB_MODEL,

        messages=[
            {
                "role": "system",
                "content": (
                    "You are a financial market "
                    "research assistant. "
                    "Use web-grounded information "
                    "when available. "
                    "Give concise answers."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.1,

        max_tokens=1000
    )


    # --------------------------------------
    # Extract response
    # --------------------------------------

    message = response.choices[0].message

    answer = message.content


    # --------------------------------------
    # Extract sources
    # --------------------------------------

    sources = []


    executed_tools = getattr(
        message,
        "executed_tools",
        None
    )


    if executed_tools:

        for tool in executed_tools:

            search_results = getattr(
                tool,
                "search_results",
                None
            )

            if search_results:

                sources.append(
                    search_results
                )


    return {
        "answer": answer,
        "sources": sources
    }