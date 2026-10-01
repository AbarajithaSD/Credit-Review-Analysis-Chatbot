#step17
import os
import pandas as pd


from database.connection import get_connection


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

FILE_PATH = os.path.join(
    BASE_DIR,
    "data",
    "Credit_Customers_data.xlsx"
)


def clean_value(value):

    if pd.isna(value):
        return None

    if isinstance(value, pd.Timestamp):
        return value.to_pydatetime()

    if hasattr(value, "item"):
        return value.item()

    return value


def import_excel():

    print(
        f"Reading Excel file: {FILE_PATH}"
    )

    df = pd.read_excel(FILE_PATH)

    print(
        f"Rows found: {len(df)}"
    )

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM customers"
    )

    insert_query = """
        INSERT INTO customers (
            customer_code,
            customer_name,
            business_currency,
            credit_limit,
            company_books_credit_limit,
            customer_credit_rating,
            invoice_balance,
            ncnr_percentage,
            payment_terms,
            total_efx_exposure,
            ar_balance,
            past_due_amount,
            customer_status,
            ap_balance,
            raw_material,
            raw_material_after_ncnr,
            wip,
            finished_goods,
            open_po_balance,
            open_po_balance_ncnr,
            cancellation_fees,
            invoice_raw_material,
            inv_date
        )
        VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s
        )
    """

    for _, row in df.iterrows():

        values = (

            clean_value(
                row["customer code"]
            ),

            clean_value(
                row["Customer name"]
            ),

            clean_value(
                row["business currency"]
            ),

            clean_value(
                row["credit limit"]
            ),

            clean_value(
                row["company books credit limit"]
            ),

            clean_value(
                row["customer credit rating"]
            ),

            clean_value(
                row["invoice balance"]
            ),

            clean_value(
                row["NCNR percentage"]
            ),

            clean_value(
                row["payment terms"]
            ),

            clean_value(
                row["TOTAL_EFX_EXPOSURE"]
            ),

            clean_value(
                row["AR balance"]
            ),

            clean_value(
                row["Past Due amount"]
            ),

            clean_value(
                row["customer status"]
            ),

            clean_value(
                row["AP balance"]
            ),

            clean_value(
                row["raw material"]
            ),

            clean_value(
                row["raw material after NCNR"]
            ),

            clean_value(
                row["WIP"]
            ),

            clean_value(
                row["Finished Goods"]
            ),

            clean_value(
                row["Open PO balance"]
            ),

            clean_value(
                row["Open PO balance NCNR"]
            ),

            clean_value(
                row["cancellation fees"]
            ),

            clean_value(
                row["Invoice Raw material"]
            ),

            clean_value(
                row["INV_DATE"]
            )
        )

        cursor.execute(
            insert_query,
            values
        )

    connection.commit()

    cursor.close()
    connection.close()

    print(
        f"Successfully imported {len(df)} records."
    )


if __name__ == "__main__":

    import_excel()