# spreadsheet-automator/create_sample_input.py
"""
Creates data/input_sales.xlsx with the sample sales data from the lab sheet.
An empty row is left on purpose to show that the processor skips it.
"""
import os
import openpyxl
from openpyxl.styles import Font

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

ROWS = [
    ("Product Name", "Quantity", "Unit Price"),
    ("Laptop", 2, 1200.50),
    ("Mouse", 5, 25.00),
    ("Keyboard", 3, 75.99),
    ("Monitor", 1, 300.00),
    (None, None, None),  # empty row (intentional)
    ("Printer", 1, 150.00),
]


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Sheet1"
    for row in ROWS:
        ws.append(row)
    for cell in ws[1]:
        cell.font = Font(bold=True)
    path = os.path.join(DATA_DIR, 'input_sales.xlsx')
    wb.save(path)
    print(f"Sample input created at '{path}'.")


if __name__ == "__main__":
    main()
