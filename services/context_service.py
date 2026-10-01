# services/context_service.py


MAX_MEMORY_CHARS = 12000

MAX_SUMMARY_CHARS = 4000

MAX_DATABASE_CHARS = 8000

MAX_WEB_CHARS = 8000

MAX_QUESTION_CHARS = 3000


def limit_text(
    text,
    max_chars
):

    if text is None:
        return ""

    text = str(text)

    if len(text) <= max_chars:
        return text

    return (
        text[:max_chars]
        + "\n\n[Content truncated]"
    )


def limit_question(question):

    return limit_text(
        question,
        MAX_QUESTION_CHARS
    )


def limit_memory(memory):

    return limit_text(
        memory,
        MAX_MEMORY_CHARS
    )


def limit_summary(summary):

    return limit_text(
        summary,
        MAX_SUMMARY_CHARS
    )


def limit_database_result(data):

    return limit_text(
        data,
        MAX_DATABASE_CHARS
    )


def limit_web_result(data):

    return limit_text(
        data,
        MAX_WEB_CHARS
    )