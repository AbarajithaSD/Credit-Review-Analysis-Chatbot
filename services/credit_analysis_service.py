def analyze_customer(customer):

    credit_limit = (
        customer["credit_limit"] or 0
    )

    exposure = (
        customer["total_efx_exposure"] or 0
    )

    past_due = (
        customer["past_due_amount"] or 0
    )

    ar_balance = (
        customer["ar_balance"] or 0
    )

    if credit_limit > 0:

        exposure_ratio = (
            exposure /
            credit_limit
        ) * 100

    else:

        exposure_ratio = None


    if ar_balance > 0:

        past_due_ratio = (
            past_due /
            ar_balance
        ) * 100

    else:

        past_due_ratio = None


    return {

        "exposure_ratio":
            exposure_ratio,

        "past_due_ratio":
            past_due_ratio
    }


def risk_level(exposure_ratio):

    if exposure_ratio is None:

        return "Unknown"

    if exposure_ratio >= 100:

        return "Critical"

    if exposure_ratio >= 90:

        return "High"

    if exposure_ratio >= 75:

        return "Moderate-High"

    if exposure_ratio >= 50:

        return "Moderate"

    return "Low"

