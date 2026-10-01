import sys
import os


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(
    0,
    PROJECT_ROOT
)


from services.web_service import web_search


question = (
    "What is the current RBI repo rate?"
)


try:

    result = web_search(
        question=question
    )

    print("\n" + "=" * 60)

    print("WEB SEARCH TEST SUCCESSFUL")

    print("=" * 60)

    print("\nANSWER:\n")

    print(result["answer"])

    print("\nSOURCES:\n")

    print(result["sources"])


except Exception as e:

    print("\n" + "=" * 60)

    print("WEB SEARCH TEST FAILED")

    print("=" * 60)

    print("\nERROR TYPE:")

    print(type(e).__name__)

    print("\nERROR:")

    print(e)