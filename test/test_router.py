import sys
import os


# Add project root to Python path
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(
    0,
    PROJECT_ROOT
)


from services.router_service import classify_question


questions = [

    "Show me the credit history of customer 1001.",

    "What is the current RBI repo rate?",

    "What is the current interest rate for home loans in India?",

    "Hello, how are you?"

]


for question in questions:

    print("\n" + "=" * 60)

    print("QUESTION:")
    print(question)

    print("=" * 60)


    try:

        result = classify_question(
            question
        )

        print("\nROUTER RESULT:")
        print(result)


    except Exception as e:

        print("\nERROR:")
        print(type(e).__name__)

        print(e)