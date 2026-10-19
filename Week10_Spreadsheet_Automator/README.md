# Week 10 LabX BASIC: Automating Spreadsheets (Excel & Google Sheets)

This project demonstrates how to programmatically interact with Microsoft Excel `.xlsx` files using Python's `openpyxl` library. It includes functionalities to read data from an existing spreadsheet, perform calculations, and write formatted results to a new Excel file.

## Key Concepts Demonstrated

* **`openpyxl` Library**: Core library for reading, writing, and modifying Excel `.xlsx` files.
* **Workbook & Worksheet Management**: Loading, creating, and saving Excel workbooks; accessing and creating sheets.
* **Cell Manipulation**: Reading and writing cell values by coordinates or cell names.
* **Data Processing**: Iterating through rows, performing calculations (e.g., total sales).
* **Basic Formatting**: Applying fonts, fills, borders, and number formats to cells.
* **Column Width Adjustment**: Dynamically adjusting column widths for readability.

## Setup & How to Run

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/sapphanyu/Week10_LabX-BASIC_-Automating.git
    cd Week10_LabX-BASIC_-Automating/spreadsheet-automator
    ```
2.  **Install Dependencies:**
    It's highly recommended to use a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate.bat
    pip install openpyxl
    ```
3.  **Prepare Input Data:**
    * A ready-made `data/input_sales.xlsx` is included. To regenerate it, run `python create_sample_input.py`.
    * Or create it manually: make a folder named `data` in the root of your project: `mkdir data`.
    * Inside the `data` folder, create an Excel file named `input_sales.xlsx`.
    * Populate `input_sales.xlsx` with sample sales data. The script expects the first sheet to have headers "Product Name", "Quantity", and "Unit Price" in cells A1, B1, C1 respectively, and data starting from row 2.

    **Example `input_sales.xlsx` content:**

    | Product Name | Quantity | Unit Price |
    | :----------- | :------- | :--------- |
    | Laptop       | 2        | 1200.50    |
    | Mouse        | 5        | 25.00      |
    | Keyboard     | 3        | 75.99      |
    | Monitor      | 1        | 300.00     |
    |              |          |            |
    | Printer      | 1        | 150.00     |

4.  **Run the script:**
    ```bash
    python main.py
    ```
    The script will:
    * Load `input_sales.xlsx`.
    * Calculate total prices per item and a grand total.
    * Create `output_sales_report.xlsx` in the `data` folder with the processed data and formatting.

    **Expected output (`data/output_sales_report.xlsx`, sheet "Sales Report"):**

    | Product Name | Quantity | Unit Price | Total Price |
    | :----------- | -------: | ---------: | ----------: |
    | Laptop       | 2        | 1,200.50   | 2,401.00    |
    | Mouse        | 5        | 25.00      | 125.00      |
    | Keyboard     | 3        | 75.99      | 227.97      |
    | Monitor      | 1        | 300.00     | 300.00      |
    | Printer      | 1        | 150.00     | 150.00      |
    | **Grand Total:** (merged A–C) | | | **3,203.97** |

    Formatting: header row bold white on green, grand-total row bold on yellow, thin borders, `#,##0.00` number format, auto-sized columns. The empty row in the input is skipped.

## Project Structure

```
spreadsheet-automator/
├── src/
│   ├── __init__.py              # Python package marker
│   ├── excel_processor.py       # Core logic for Excel file reading/writing/processing
│   └── data_models.py           # (Optional) SalesItem dataclass for structured rows
├── data/
│   ├── input_sales.xlsx         # Sample input Excel file
│   └── output_sales_report.xlsx # Generated output Excel file
├── create_sample_input.py       # Helper that builds data/input_sales.xlsx
├── main.py                      # Application entry point
├── .gitignore                   # Files/folders to ignore in Git
└── README.md                    # This project overview
```

## Debugging Spreadsheet Automation

* **`FileNotFoundError`**: Ensure your `input_sales.xlsx` file is correctly placed in the `data` directory and its name matches exactly.
* **`InvalidFileException` (or similar `openpyxl` error)**: This often means the Excel file is corrupted, or it's not a valid `.xlsx` file (e.g., it's an old `.xls` format, which `openpyxl` doesn't support). Ensure you are saving as `.xlsx`.
* **`IndexError` or `TypeError`**: If your script expects a number but gets text (or vice versa), or if it tries to access a row/column that doesn't exist, these errors can occur. Add `try-except` blocks around data type conversions and checks for `None` values.
* **Data Mismatches**: The script assumes a specific column order (Product Name, Quantity, Unit Price). If your input file has a different order or missing columns, the calculations will be incorrect. Adjust the `excel_processor.py` logic to match your file's structure.
* **Formatting Issues**: If formatting doesn't appear, double-check the `openpyxl.styles` syntax. Ensure you are applying styles to the correct cell objects *before* saving.

## Conceptual Overview: Google Sheets Automation

Local `.xlsx` files are edited with `openpyxl`; cloud spreadsheets are edited through the **Google Sheets API**, usually via the `gspread` client library.

* **Authentication**: Google APIs use **OAuth 2.0**. For scripts, the common approach is a **service account** (a JSON key file from Google Cloud Console). Share the target sheet with the service account's email so it can access it.
* **Key management**: Never commit the JSON key to Git. Keep it outside the repo or in an ignored path, and load its location from an environment variable (e.g. `.env`, already in `.gitignore`).
* **Minimal example (not part of this prototype):**
    ```python
    import gspread
    gc = gspread.service_account(filename="credentials.json")
    ws = gc.open("Sales Data").sheet1
    rows = ws.get_all_values()          # read
    ws.update_acell("D1", "Total Price") # write
    ```
* **Similarities with openpyxl**: the same workbook → worksheet → cell model, A1-style addressing, reading and writing values row by row.
* **Differences**: every call is a network request (slower, rate-limited, so batch updates are preferred); requires credentials and internet; changes are live and shared with collaborators instead of saved to a local file; formatting uses a different API (`format()` / batch requests).

## Ethical & Data-Integrity Notes

* Work on a copy: the script never overwrites the input file; results go to a new file.
* Invalid rows are skipped with a warning rather than silently guessed, so totals stay trustworthy.
* Sales data may be confidential, so do not commit real customer/business data or API credentials to a public repository.

## Extension Ideas (Future Work)

* **Google Sheets Integration**: Explore the Google Sheets API (`gspread` library) to read, write, and update data in cloud-based spreadsheets. This involves setting up API credentials.
* **Automated Data Validation**: Add logic to check for missing values, out-of-range numbers, or incorrect data types in the input spreadsheet.
* **Advanced Data Analysis**: Implement more complex calculations (e.g., average sales per product, sales trends, pivot table creation via data manipulation).
* **Chart Generation**: `openpyxl` supports creating charts directly within the Excel file based on your data.
* **Conditional Formatting**: Apply rules-based formatting (e.g., highlight low stock, high sales).
* **GUI for Spreadsheet Tasks**: Create a simple graphical user interface (GUI) using `Tkinter` or `PyQt` to allow users to select input/output files and trigger processing.
* **Integration with Databases**: Read data from Excel and insert it into a database, or query a database and export results to Excel.

---


แหล่งที่มา
1. https://github.com/GideonJagen/auto-budget
2. https://github.com/KijaziAbraham/Managing-Subscription-Payment
3. https://github.com/MikeyBeez/RAGAgent
4. https://automatetheboringstuff.com/2e/chapter13/
