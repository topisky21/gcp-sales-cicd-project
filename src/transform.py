
from datetime import date
from decimal import Decimal, InvalidOperation


def transform_sale(record: dict) -> dict:
    """
    Validate and transform one sales record
    into the format expected by BigQuery.
    """

    required_fields = [
        "order_id",
        "order_date",
        "product",
        "quantity",
        "unit_price",
    ]

    # Check that all required fields are present.
    missing_fields = [
        field for field in required_fields
        if field not in record or record[field] is None
    ]

    if missing_fields:
        raise ValueError(
            f"Missing required fields: {', '.join(missing_fields)}"
        )

    # Validate order ID.
    order_id = str(record["order_id"]).strip()

    if not order_id:
        raise ValueError("order_id cannot be empty")

    # Validate order date.
    try:
        order_date = date.fromisoformat(str(record["order_date"]))
    except (ValueError, TypeError):
        raise ValueError(
            "order_date must use YYYY-MM-DD format"
        )

    # Validate product name.
    product = str(record["product"]).strip()

    if not product:
        raise ValueError("product cannot be empty")

    # Validate quantity without silently truncating decimals.
    try:
        quantity_value = Decimal(str(record["quantity"]))

        if not quantity_value.is_finite():
            raise ValueError

        if quantity_value != quantity_value.to_integral_value():
            raise ValueError

        quantity = int(quantity_value)

    except (InvalidOperation, ValueError, TypeError):
        raise ValueError("quantity must be a whole number")

    if quantity <= 0:
        raise ValueError("quantity must be greater than zero")

    # Validate unit price using Decimal for accuracy.
    try:
        unit_price = Decimal(str(record["unit_price"]))

        if not unit_price.is_finite():
            raise ValueError

    except (InvalidOperation, ValueError, TypeError):
        raise ValueError("unit_price must be a valid number")

    if unit_price < 0:
        raise ValueError("unit_price cannot be negative")

    if unit_price >= Decimal("1e29"):
        raise ValueError("unit_price exceeds BigQuery NUMERIC range")

    if unit_price.as_tuple().exponent < -9:
        raise ValueError(
            "unit_price cannot have more than 9 decimal places"
        )

    # Return only fields matching the BigQuery table schema.
    return {
        "order_id": order_id,
        "order_date": order_date.isoformat(),
        "product": product,
        "quantity": quantity,
        "unit_price": str(unit_price),
    }
