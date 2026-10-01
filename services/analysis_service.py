#step28
from services.llm_service import generate_response
from services.database_service import (
    execute_select
)


import json

from services.context_service import (
    limit_database_result
)


def generate_sql(question):

    schema = """
customers table:

customer_code
customer_name
business_currency
credit_limit
company_books_credit_limit
customer_credit_rating
invoice_balance
ncnr_percentage
payment_terms
total_efx_exposure
ar_balance
past_due_amount
customer_status
ap_balance
raw_material
raw_material_after_ncnr
wip
finished_goods
open_po_balance
open_po_balance_ncnr
cancellation_fees
invoice_raw_material
inv_date
"""

    prompt = f"""
You generate safe MySQL SELECT queries.

Database schema:

{schema}

User question:

{question}

Rules:

1. Generate ONLY SELECT queries.
2. Never use INSERT.
3. Never use UPDATE.
4. Never use DELETE.
5. Never use DROP.
6. Never use ALTER.
7. Never use CREATE.
8. Never use TRUNCATE.
9. Only query the customers table.
10. Return ONLY SQL.
"""

    sql = generate_response(
        system_prompt=(
            "You are a SQL generation assistant."
        ),
        user_prompt=prompt
    )

    sql = sql.strip()

    sql = sql.replace(
        "```sql",
        ""
    ).replace(
        "```",
        ""
    ).strip()

    if sql.endswith(";"):
        sql = sql[:-1].strip()

    return sql


def validate_sql(sql):

    normalized = sql.strip().upper()

    if not normalized.startswith("SELECT"):
        return False

    if ";" in normalized:
        return False

    forbidden = [
        "INSERT",
        "UPDATE",
        "DELETE",
        "DROP",
        "ALTER",
        "CREATE",
        "TRUNCATE",
        "REPLACE",
        "GRANT",
        "REVOKE",
        "INTO OUTFILE",
        "INTO DUMPFILE",
        "FOR UPDATE"
    ]

    for word in forbidden:

        if word in normalized:
            return False

    return True


def database_analysis(question):

    sql = generate_sql(question)

    if not validate_sql(sql):

        return {
            "success": False,
            "sql": sql,
            "data": []
        }

    data = execute_select(sql)

    return {
        "success": True,
        "sql": sql,
        "data": data
    }


#step29
def generate_credit_answer(
    question,
    database_data,
    web_data,
    memory
):

    prompt = f"""
You are an expert Credit Review Analysis Assistant.

You must answer the user's question using the
available evidence.

USER QUESTION:
{question}

CONVERSATION MEMORY:
{memory}

HISTORICAL DATABASE DATA:
{limit_database_result(
    json.dumps(
        database_data,
        default=str
    )
)}

CURRENT WEB INFORMATION:
{web_data}

Rules:

1. Do not invent financial numbers.
2. Do not invent customer information.
3. Clearly distinguish historical data from current data.
4. If database data is available, use it.
5. If current web information is available, use it.
6. If both are available, compare them.
7. Summarize the result clearly.
8. Highlight credit risk indicators.
9. Mention important missing data.
10. If information is insufficient, say so.
11. Do not present assumptions as facts.
12. Use financial and credit-review terminology.
13. Do not provide a final lending decision unless
    the available evidence supports it.
14. Give a concise but useful analysis.

Return the answer in this structure:

Summary:
...

Historical Data:
...

Current Market Data:
...

Credit Risk Analysis:
...

Key Findings:
...

Data Limitations:
...
"""

    return generate_response(
        system_prompt=(
            "You are a professional credit review "
            "analysis assistant."
        ),
        user_prompt=prompt
    )


#step30
from services.router_service import classify_question
from services.web_service import web_search
from services.memory_service import build_memory
from services.analysis_service import (
    database_analysis,
    generate_credit_answer
)


def process_question(
    session_uuid,
    question
):

    memory = build_memory(
        session_uuid
    )

    route = classify_question(
        question,
        memory
    )

    database_data = []

    web_data = ""

    if route in (
        "DATABASE",
        "BOTH"
    ):

        result = database_analysis(
            question
        )

        if result["success"]:
            database_data = result["data"]

    if route == "DATABASE" and not database_data:

        route = "WEB"

    if route in (
        "WEB",
        "BOTH"
    ):

        web_result = web_search(
            question,
            memory
        )

        web_data = web_result["answer"]

    answer = generate_credit_answer(
        question=question,
        database_data=database_data,
        web_data=web_data,
        memory=memory
    )

    return {
        "answer": answer,
        "route": route,
        "database_data": database_data,
        "web_data": web_data
    }


def calculate_exposure_ratio(
    exposure,
    credit_limit
):

    if not credit_limit:

        return None

    return (
        exposure /
        credit_limit
    ) * 100