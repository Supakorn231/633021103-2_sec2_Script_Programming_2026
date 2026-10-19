import os
import sys

# Add the src directory to Python's import path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from csv_handler import CSVHandler
from json_handler import JSONHandler
from utils import setup_logging, ensure_directory_exists

logger = setup_logging(__name__)


def main():
    """Run the CSV and JSON data-processing workflows."""
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    ensure_directory_exists(data_dir)

    input_csv_path = os.path.join(data_dir, "input_sales.csv")
    output_csv_path = os.path.join(data_dir, "output_filtered_sales.csv")
    input_json_path = os.path.join(data_dir, "input_inventory.json")
    output_json_path = os.path.join(data_dir, "output_updated_inventory.json")

    csv_proc = CSVHandler()
    json_proc = JSONHandler()

    # ---------------- CSV PROCESSING ----------------
    logger.info("--- Starting CSV Data Processing Workflow ---")
    sales_data = csv_proc.read_csv_as_dicts(input_csv_path)

    if sales_data:
        min_amount_for_filter = 100.0
        processed_results = csv_proc.process_sales_data(
            sales_data, min_sale_amount=min_amount_for_filter
        )
        filtered_sales = processed_results["filtered_sales"]
        sales_summary = processed_results["summary"]

        logger.info("Summary of all sales: %s", sales_summary)

        csv_fieldnames = list(sales_data[0].keys())
        summary_row = {
            "OrderID": "SUMMARY",
            "Product": "Total/Avg",
            "Amount": sales_summary["Total Sales"],
            "Price": sales_summary["Average Item Price"],
            "Customer": f'Count: {sales_summary["Filtered Sales Count"]}',
        }
        filtered_sales_with_summary = filtered_sales + [summary_row]

        csv_proc.write_dicts_to_csv(
            filtered_sales_with_summary, output_csv_path, csv_fieldnames
        )
    else:
        logger.error("No sales data to process from CSV.")

    # ---------------- JSON PROCESSING ----------------
    logger.info("--- Starting JSON Data Processing Workflow ---")
    inventory_data = json_proc.read_json(input_json_path)

    if inventory_data:
        json_proc.update_inventory(inventory_data, "PROD001", 60)
        json_proc.update_inventory(inventory_data, "PROD003", 75)

        new_product_entry = {
            "id": "PROD004",
            "name": "Gaming Headset",
            "category": "Audio",
            "stock": 90,
            "details": {
                "brand": "SoundBlaster",
                "features": ["Noise Cancelling", "RGB"],
            },
        }
        json_proc.add_product(inventory_data, new_product_entry)
        json_proc.write_json(inventory_data, output_json_path, indent=2)
    else:
        logger.error("No inventory data to process from JSON.")

    logger.info("--- Data Processing Workflows Completed ---")


if __name__ == "__main__":
    main()
