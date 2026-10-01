#step24
from services.llm_service import generate_response


ROUTER_PROMPT = """
You are a question-routing classifier for a credit
review analysis chatbot.

Classify the user's question into exactly one category:

DATABASE
WEB
BOTH

DATABASE:
Use when the answer can be obtained from the historical
customer credit database.

WEB:
Use when the question requires current internet information,
current market conditions, current company news, current
economic conditions, current interest rates, current events,
or other live information.

BOTH:
Use when the answer requires historical database information
AND current internet information.

Return ONLY:

DATABASE

or

WEB

or

BOTH
"""


def classify_question(
    question,
    memory=""
):

    user_prompt = f"""
CONVERSATION MEMORY:
{memory}

CURRENT USER QUESTION:
{question}

Classify the current question as DATABASE, WEB, or BOTH.

If the question refers to previous conversation context,
use the conversation memory to determine what the user means.

Return ONLY:
DATABASE
WEB
or
BOTH
"""

    result = generate_response(
        system_prompt=ROUTER_PROMPT,
        user_prompt=user_prompt
    )

    result = result.strip().upper()

    if "BOTH" in result:
        return "BOTH"

    if "WEB" in result:
        return "WEB"

    return "DATABASE"