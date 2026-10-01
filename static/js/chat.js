const chatContainer =
    document.getElementById(
        "chatContainer"
    );

const chatForm =
    document.getElementById(
        "chatForm"
    );

const messageInput =
    document.getElementById(
        "messageInput"
    );

const sendButton =
    document.getElementById(
        "sendButton"
    );

const endChatButton =
    document.getElementById(
        "endChatButton"
    );

const typingIndicator =
    document.getElementById(
        "typingIndicator"
    );

const endedMessage =
    document.getElementById(
        "endedMessage"
    );


let sessionUuid =
    localStorage.getItem(
        "credit_chat_session_uuid"
    );


function createUUID() {

    return crypto.randomUUID();

}


function addMessage(
    role,
    message
) {

    const messageElement =
        document.createElement(
            "div"
        );

    messageElement.className =
        `message ${role}`;

    const content =
        document.createElement(
            "div"
        );

    content.className =
        "message-content";

    content.textContent =
        message;

    messageElement.appendChild(
        content
    );

    chatContainer.appendChild(
        messageElement
    );

    chatContainer.scrollTop =
        chatContainer.scrollHeight;

}


async function createSession() {

    if (!sessionUuid) {

        sessionUuid =
            createUUID();

        localStorage.setItem(
            "credit_chat_session_uuid",
            sessionUuid
        );

    }

    const response =
        await fetch(
            "/api/session",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    session_uuid:
                        sessionUuid
                })
            }
        );

    const data =
        await response.json();

    if (!data.success) {

        throw new Error(
            data.error
        );

    }

    if (
        data.session.status ===
        "ended"
    ) {

        disableChat();

    }

}


async function loadHistory() {

    const response =
        await fetch(
            `/api/history/${sessionUuid}`
        );

    const data =
        await response.json();

    if (!data.success) {

        return;

    }

    chatContainer.innerHTML = "";

    data.messages.forEach(
        item => {

            addMessage(
                item.role,
                item.message
            );

        }
    );

    if (
        data.session.status ===
        "ended"
    ) {

        disableChat();

    }

}


function disableChat() {

    messageInput.disabled =
        true;

    sendButton.disabled =
        true;

    endChatButton.disabled =
        true;

    endedMessage.classList.remove(
        "hidden"
    );

}


function enableLoading() {

    typingIndicator.classList.remove(
        "hidden"
    );

    sendButton.disabled =
        true;

}


function disableLoading() {

    typingIndicator.classList.add(
        "hidden"
    );

    sendButton.disabled =
        false;

}


chatForm.addEventListener(
    "submit",
    async function(event) {

        event.preventDefault();

        const message =
            messageInput.value.trim();

        if (!message) {

            return;

        }

        addMessage(
            "user",
            message
        );

        messageInput.value = "";

        enableLoading();

        try {

            const response =
                await fetch(
                    "/api/chat",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify({
                                session_uuid:
                                    sessionUuid,

                                message:
                                    message
                            })
                    }
                );

            const data =
                await response.json();

            if (!data.success) {

                addMessage(
                    "assistant",
                    `Error: ${data.error}`
                );

                return;

            }

            addMessage(
                "assistant",
                data.answer
            );

        }
        catch (error) {

            addMessage(
                "assistant",
                "An unexpected error occurred."
            );

            console.error(error);

        }
        finally {

            disableLoading();

        }

    }
);


endChatButton.addEventListener(
    "click",
    async function() {

        const confirmed =
            confirm(
                "Are you sure you want to end this chat?"
            );

        if (!confirmed) {
            return;
        }

        try {

            const response =
                await fetch(
                    "/api/end-chat",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({
                            session_uuid:
                                sessionUuid
                        })
                    }
                );

            const data =
                await response.json();

            if (!data.success) {

                alert(
                    data.error ||
                    "Unable to end chat."
                );

                return;

            }

            disableChat();

            const newChat =
                confirm(
                    "Chat ended successfully. Start a new chat?"
                );

            if (newChat) {

                localStorage.removeItem(
                    "credit_chat_session_uuid"
                );

                window.location.reload();

            }

        }
        catch (error) {

            console.error(error);

            alert(
                "Unable to end chat."
            );

        }

    }
);


async function initialize() {

    try {

        await createSession();

        await loadHistory();

    }
    catch (error) {

        console.error(error);

        addMessage(
            "assistant",
            "Unable to initialize the chat."
        );

    }

}


initialize();