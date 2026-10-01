# services/memory_service.py

from services.llm_service import generate_response

from services.database_service import (
    get_recent_messages,
    get_previous_summaries
)

from services.context_service import (
    limit_memory,
    limit_summary
)


def build_memory(session_uuid):

    messages = get_recent_messages(
        session_uuid,
        limit=10
    )

    summaries = get_previous_summaries(
        session_uuid,
        limit=3
    )

    memory_parts = []

    if summaries:

        summary_text = ""

        for item in summaries:

            summary_text += (
                f"- {item['summary']}\n"
            )

        summary_text = limit_summary(
            summary_text
        )

        memory_parts.append(
            "PREVIOUS CHAT SUMMARIES:\n"
            + summary_text
        )

    if messages:

        history_text = ""

        for item in messages:

            history_text += (
                f"{item['role'].upper()}: "
                f"{item['message']}\n"
            )

        memory_parts.append(
            "RECENT CHAT HISTORY:\n"
            + history_text
        )

    memory = "\n\n".join(
        memory_parts
    )

    return limit_memory(
        memory
    )


def generate_chat_summary(session_uuid):

    messages = get_recent_messages(
        session_uuid,
        limit=50
    )

    if not messages:
        return None

    conversation = ""

    for item in messages:

        conversation += (
            f"{item['role'].upper()}: "
            f"{item['message']}\n"
        )

    conversation = limit_memory(
        conversation
    )

    prompt = f"""
Summarize this credit review chatbot conversation.

Include:

1. Customers discussed
2. Credit risks identified
3. Financial metrics discussed
4. Important user questions
5. Important conclusions
6. Current market information discussed
7. Unresolved questions
8. Important context for future conversations

Conversation:

{conversation}
"""

    summary = generate_response(
        system_prompt=(
            "You are a credit review "
            "conversation memory "
            "summarization assistant."
        ),
        user_prompt=prompt,
        temperature=0.2,
        max_tokens=700
    )

    return limit_summary(
        summary
    )