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


from config import Config
from groq import Groq


print("CONFIG FILE:")
print(Config.__module__)

print("\nGROQ API KEY LOADED:")
print(bool(Config.GROQ_API_KEY))

print("\nGROQ MODEL:")
print(Config.GROQ_MODEL)


client = Groq(
    api_key=Config.GROQ_API_KEY
)


print("\nAVAILABLE GROQ MODELS:\n")


models = client.models.list()


for model in models.data:

    print(
        f"{model.id} | "
        f"active={model.active}"
    )