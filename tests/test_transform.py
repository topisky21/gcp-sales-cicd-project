
import unittest

from src.transform import transform_sale


class TestTransformSale(unittest.TestCase):

    def setUp(self):
        self.valid_record = {
            "order_id": "ORD-001",
            "order_date": "2026-11-10",
            "product": "Laptop",
            "quantity": 2,
            "unit_price": "750.50",
        }

    def test_valid_sales_record(self):
        result = transform_sale(self.valid_record)

        self.assertEqual(result["order_id"], "ORD-001")
        self.assertEqual(result["order_date"], "2026-11-10")
        self.assertEqual(result["product"], "Laptop")
        self.assertEqual(result["quantity"], 2)
        self.assertEqual(result["unit_price"], "750.50")

    def test_missing_order_id_is_rejected(self):
        record = self.valid_record.copy()
        del record["order_id"]

        with self.assertRaises(ValueError):
            transform_sale(record)

    def test_zero_quantity_is_rejected(self):
        record = self.valid_record.copy()
        record["quantity"] = 0

        with self.assertRaises(ValueError):
            transform_sale(record)

    def test_negative_quantity_is_rejected(self):
        record = self.valid_record.copy()
        record["quantity"] = -2

        with self.assertRaises(ValueError):
            transform_sale(record)

    def test_invalid_date_is_rejected(self):
        record = self.valid_record.copy()
        record["order_date"] = "not-a-date"

        with self.assertRaises(ValueError):
            transform_sale(record)

    def test_negative_unit_price_is_rejected(self):
        record = self.valid_record.copy()
        record["unit_price"] = "-10.50"

        with self.assertRaises(ValueError):
            transform_sale(record)

    def test_empty_product_is_rejected(self):
        record = self.valid_record.copy()
        record["product"] = "   "

        with self.assertRaises(ValueError):
            transform_sale(record)

    def test_decimal_quantity_is_rejected(self):
        record = self.valid_record.copy()
        record["quantity"] = 2.5

        with self.assertRaises(ValueError):
            transform_sale(record)


if __name__ == "__main__":
    unittest.main()
