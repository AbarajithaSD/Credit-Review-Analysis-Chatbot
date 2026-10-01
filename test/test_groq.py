import sys
import os


# Add project root to Python import path
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(
    0,
    PROJECT_ROOT
)


from services.llm_service import generate_response


answer = generate_response(
    system_prompt=(
        "You are a helpful AI assistant. "
        "Answer clearly and concisely."
    ),
    user_prompt=(
        "Explain what a credit score is."
    ),
    max_tokens=300
)


print("\nLLM RESPONSE:")
print(answer)