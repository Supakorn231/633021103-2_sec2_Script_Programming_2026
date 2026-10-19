# spreadsheet-automator/src/data_models.py
"""
(Optional) Structured data models for the sales processor.
Using a dataclass keeps each row's data typed and makes calculations explicit.
"""
from dataclasses import dataclass


@dataclass
class SalesItem:
    """One row of sales data: Product Name, Quantity, Unit Price."""
    product_name: str
    quantity: int
    unit_price: float

    @property
    def total_price(self) -> float:
        """Total price for this item (quantity x unit price)."""
        return round(self.quantity * self.unit_price, 2)

    @classmethod
    def from_row(cls, row):
        """
        Build a SalesItem from a tuple of cell values (values_only=True).
        Raises ValueError/TypeError if the numbers are invalid.
        """
        product_name = row[0] if len(row) > 0 else None
        quantity = int(row[1] if len(row) > 1 else 0)
        unit_price = float(row[2] if len(row) > 2 else 0.0)
        return cls(product_name, quantity, unit_price)
