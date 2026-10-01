#step31

from flask import (
    Flask,
    render_template,
    request,
    jsonify
)

from services.database_service import (
    create_chat_session,
    get_session,
    save_message,
    end_chat,
    get_recent_messages
)

from services.analysis_service import (
    process_question
)

from services.memory_service import (
    generate_chat_summary
)

from database.connection import get_connection


app = Flask(__name__)


@app.route("/")
def index():

    return render_template(
        "index.html"
    )


@app.route(
    "/api/session",
    methods=["POST"]
)
def create_session():

    data = request.get_json(
        silent=True
    ) or {}

    session_uuid = data.get(
        "session_uuid"
    )

    if not session_uuid:

        return jsonify({
            "success": False,
            "error": "session_uuid is required"
        }), 400

    existing = get_session(
        session_uuid
    )

    if existing:

        return jsonify({
            "success": True,
            "session": existing
        })

    create_chat_session(
        session_uuid
    )

    session = get_session(
        session_uuid
    )

    return jsonify({
        "success": True,
        "session": session
    })


@app.route("/api/chat", methods=["POST"])
def chat():

    data = request.get_json(silent=True) or {}

    question = data.get("message", "").strip()

    session_uuid = data.get("session_uuid")

    if not question:
        return jsonify({
            "success": False,
            "error": "Message is required"
        }), 400

    if not session_uuid:
        return jsonify({
            "success": False,
            "error": "Session UUID is required"
        }), 400

    session = get_session(session_uuid)

    if not session:
        return jsonify({
            "success": False,
            "error": "Chat session not found"
        }), 404

    if session["status"] == "ended":
        return jsonify({
            "success": False,
            "error": "This chat has ended."
        }), 400

    save_message(
        session_uuid,
        "user",
        question,
        "general"
    )

    result = process_question(
        session_uuid,
        question
    )

    if result["route"] == "DATABASE":
        source_type = "database"

    elif result["route"] == "WEB":
        source_type = "web"

    elif result["route"] == "BOTH":
        source_type = "database_web"

    else:
        source_type = "general"

    save_message(
        session_uuid,
        "assistant",
        result["answer"],
        source_type
    )

    return jsonify({
        "success": True,
        "answer": result["answer"],
        "route": result["route"]
    })


@app.route(
    "/api/history/<session_uuid>",
    methods=["GET"]
)
def history(session_uuid):

    session = get_session(
        session_uuid
    )

    if not session:

        return jsonify({
            "success": False,
            "error": "Session not found"
        }), 404

    messages = get_recent_messages(
        session_uuid,
        limit=100
    )

    return jsonify ({
        "success": True,
        "session": session,
        "messages": messages
    })


@app.route(
    "/api/end-chat",
    methods=["POST"]
)
def finish_chat():

    data = request.get_json(
        silent=True
    ) or {}

    session_uuid = data.get(
        "session_uuid"
    )

    if not session_uuid:

        return jsonify({
            "success": False,
            "error": "Missing session_uuid"
        }), 400

    session = get_session(
        session_uuid
    )

    if not session:

        return jsonify({
            "success": False,
            "error": "Session not found"
        }), 404

    try:

        summary = generate_chat_summary(
            session_uuid
        )

        if summary:

            from services.database_service import (
                save_summary
            )

            save_summary(
                session_uuid,
                summary
            )

    except Exception as error:

        print(
            f"Summary error: {error}"
        )

    end_chat(
        session_uuid
    )

    return jsonify({
        "success": True,
        "message": "Chat ended successfully."
    })


@app.route(
    "/api/health",
    methods=["GET"]
)
def health():

    try:

        connection = get_connection()

        connection.close()

        return jsonify({
            "status": "healthy",
            "database": "connected"
        })

    except Exception as error:

        return jsonify({
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(error)
        }), 500


if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )