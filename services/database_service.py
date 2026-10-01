# services/database_service.py

from database.connection import get_connection


def execute_select(query, params=None):
    connection = get_connection()

    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(query, params or ())
        results = cursor.fetchall()
        return results

    finally:
        cursor.close()
        connection.close()


def get_customer_by_name(name):
    query = """
        SELECT *
        FROM customers
        WHERE customer_name LIKE %s
        LIMIT 20
    """

    return execute_select(
        query,
        (f"%{name}%",)
    )


def get_customer_by_code(code):
    query = """
        SELECT *
        FROM customers
        WHERE customer_code = %s
        LIMIT 1
    """

    results = execute_select(
        query,
        (code,)
    )

    if results:
        return results[0]

    return None


def get_recent_messages(session_uuid, limit=10):
    query = """
        SELECT
            m.role,
            m.message,
            m.created_at
        FROM chat_messages m
        JOIN chat_sessions s
            ON m.session_id = s.id
        WHERE s.session_uuid = %s
        ORDER BY m.created_at DESC
        LIMIT %s
    """

    results = execute_select(
        query,
        (
            session_uuid,
            limit
        )
    )

    return list(reversed(results))


def get_previous_summaries(session_uuid, limit=5):

    query = """
        SELECT
            cs.id,
            cs.summary
        FROM chat_summaries cs
        JOIN chat_sessions s
            ON cs.session_id = s.id
        WHERE s.session_uuid = %s
        ORDER BY cs.id DESC
        LIMIT %s
    """

    return execute_select(
        query,
        (
            session_uuid,
            limit
        )
    )


def create_chat_session(session_uuid):
    connection = get_connection()

    cursor = connection.cursor()

    try:
        query = """
            INSERT INTO chat_sessions (
                session_uuid,
                title,
                status
            )
            VALUES (
                %s,
                %s,
                'active'
            )
        """

        cursor.execute(
            query,
            (
                session_uuid,
                "New Credit Review"
            )
        )

        connection.commit()

    finally:
        cursor.close()
        connection.close()


def get_session(session_uuid):
    query = """
        SELECT *
        FROM chat_sessions
        WHERE session_uuid = %s
        LIMIT 1
    """

    results = execute_select(
        query,
        (session_uuid,)
    )

    if results:
        return results[0]

    return None


def save_message(
    session_uuid,
    role,
    message,
    source_type
):
    connection = get_connection()

    cursor = connection.cursor()

    try:
        query = """
            INSERT INTO chat_messages (
                session_id,
                role,
                message,
                source_type
            )
            SELECT
                id,
                %s,
                %s,
                %s
            FROM chat_sessions
            WHERE session_uuid = %s
        """

        cursor.execute(
            query,
            (
                role,
                message,
                source_type,
                session_uuid
            )
        )

        connection.commit()

    finally:
        cursor.close()
        connection.close()


def end_chat(session_uuid):
    connection = get_connection()

    cursor = connection.cursor()

    try:
        query = """
            UPDATE chat_sessions
            SET
                status = 'ended',
                ended_at = NOW()
            WHERE session_uuid = %s
        """

        cursor.execute(
            query,
            (session_uuid,)
        )

        connection.commit()

    finally:
        cursor.close()
        connection.close()


def save_summary(
    session_uuid,
    summary
):

    connection = get_connection()

    cursor = connection.cursor()

    try:

        query = """
            INSERT INTO chat_summaries (
                session_id,
                summary
            )
            SELECT
                id,
                %s
            FROM chat_sessions
            WHERE session_uuid = %s
        """

        cursor.execute(
            query,
            (
                summary,
                session_uuid
            )
        )

        connection.commit()

    finally:

        cursor.close()
        connection.close() 