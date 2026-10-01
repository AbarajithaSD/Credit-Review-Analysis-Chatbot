import sys
import os

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(0, PROJECT_ROOT)


from groq import Groq
from config import Config


print("API KEY LOADED:")
print(bool(Config.GROQ_API_KEY))


client = Groq(
    api_key=Config.GROQ_API_KEY
)


print("\nTesting Groq Compound directly...\n")


response = client.chat.completions.create(
    model="groq/compound",
    messages=[
        {
            "role": "user",
            "content": "What is the current RBI repo rate?"
        }
    ]
)


print("\nRESPONSE:\n")

print(response.choices[0].message.content)


print("\nEXECUTED TOOLS:\n")

print(
    getattr(
        response.choices[0].message,
        "executed_tools",
        None
    )
)