import csv
import os

from utils import ensure_directory_exists, setup_logging

logger = setup_logging(__name__)


class CSVHandler:
    """Read, write, and process CSV files."""

    def __init__(self):
        logger.info("CSVHandler initialized.")

    def read_csv_as_dicts(self, file_path):
        """Read a CSV file and return rows as a list of dictionaries."""
        if not os.path.exists(file_path):
            logger.error("CSV file not found: %s", file_path)
            return None

        try:
            with open(file_path, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                data = list(reader)
            logger.info("Successfully read %s rows from '%s'.", len(data), file_path)
            return data
        except (OSError, csv.Error, UnicodeError) as error:
            logger.error("Error reading CSV file '%s': %s", file_path, error)
            return None

    def write_dicts_to_csv(self, data, file_path, fieldnames):
        """Write a list of dictionaries to a CSV file."""
        if not data:
            logger.warning("No data provided to write to CSV.")
            return False

        ensure_directory_exists(os.path.dirname(file_path))
        try:
            with open(file_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            logger.info("Successfully wrote %s rows to '%s'.", len(data), file_path)
            return True
        except (OSError, csv.Error, UnicodeError) as error:
            logger.error("Error writing CSV file '%s': %s", file_path, error)
            return False

    def process_sales_data(self, sales_data, min_sale_amount=0):
        """Calculate total sales and average price, and filter sales by amount."""
        if not sales_data:
            logger.warning("No sales data provided for processing.")
            return {"filtered_sales": [], "summary": {}}

        total_sales = 0.0
        total_price = 0.0
        num_items = 0
        filtered_sales = []

        for row in sales_data:
            try:
                amount = float(row.get("Amount", 0))
                price = float(row.get("Price", 0))
                total_sales += amount
                total_price += price
                num_items += 1

                if amount >= min_sale_amount:
                    filtered_sales.append(row)
            except (ValueError, TypeError) as error:
                logger.warning("Skipping invalid row %s. Error: %s", row, error)

        average_price = total_price / num_items if num_items > 0 else 0.0
        summary = {
            "Total Sales": f"{total_sales:.2f}",
            "Average Item Price": f"{average_price:.2f}",
            "Filtered Sales Count": len(filtered_sales),
        }

        logger.info(
            "Sales data processed. Total Sales: %s, Filtered Count: %s",
            summary["Total Sales"],
            summary["Filtered Sales Count"],
        )
        return {"filtered_sales": filtered_sales, "summary": summary}
