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


from services.database_service import execute_select


query = """
SELECT *
FROM credit_customers
LIMIT 5
"""


try:

    result = execute_select(query)

    print("\nDATABASE TEST SUCCESSFUL\n")

    print(result)

except Exception as e:

    print("\nDATABASE TEST FAILED\n")

    print(type(e).__name__)

    print(e)