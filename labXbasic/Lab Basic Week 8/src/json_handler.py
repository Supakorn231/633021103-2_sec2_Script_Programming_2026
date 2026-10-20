import json
import os

from utils import ensure_directory_exists, setup_logging

logger = setup_logging(__name__)


class JSONHandler:
    """Read, write, and manipulate JSON inventory data."""

    def __init__(self):
        logger.info("JSONHandler initialized.")

    def read_json(self, file_path):
        """Read JSON from a file and return the Python object."""
        if not os.path.exists(file_path):
            logger.error("JSON file not found: %s", file_path)
            return None

        try:
            with open(file_path, mode="r", encoding="utf-8") as file:
                data = json.load(file)
            logger.info("Successfully read JSON from '%s'.", file_path)
            return data
        except json.JSONDecodeError as error:
            logger.error("Invalid JSON format in '%s': %s", file_path, error)
            return None
        except (OSError, UnicodeError) as error:
            logger.error("Error reading JSON file '%s': %s", file_path, error)
            return None

    def write_json(self, data, file_path, indent=4):
        """Write a Python object to JSON with readable indentation."""
        ensure_directory_exists(os.path.dirname(file_path))
        try:
            with open(file_path, mode="w", encoding="utf-8") as file:
                json.dump(data, file, indent=indent, ensure_ascii=False)
            logger.info("Successfully wrote JSON to '%s'.", file_path)
            return True
        except (OSError, TypeError, ValueError) as error:
            logger.error("Error writing JSON file '%s': %s", file_path, error)
            return False

    def update_inventory(self, inventory_data, product_id, new_stock_level):
        """Update the stock of a product identified by its ID."""
        if not isinstance(inventory_data, list):
            logger.warning("Inventory data is not a list. Cannot update.")
            return False

        for product in inventory_data:
            if product.get("id") == product_id:
                product["stock"] = new_stock_level
                logger.info(
                    "Updated stock for product '%s' to %s.",
                    product_id,
                    new_stock_level,
                )
                return True

        logger.warning("Product '%s' not found in inventory.", product_id)
        return False

    def add_product(self, inventory_data, new_product):
        """Append a new product to the inventory list."""
        if not isinstance(inventory_data, list):
            logger.warning("Inventory data is not a list. Cannot add product.")
            return False

        inventory_data.append(new_product)
        logger.info("Added new product: %s.", new_product.get("name", "N/A"))
        return True
