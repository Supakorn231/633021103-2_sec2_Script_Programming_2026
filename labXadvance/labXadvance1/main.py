"""Entry point: load the plan, run the agent, save results as JSON and CSV."""
import os
import sys

from src.config_parser import ConfigParser
from src.scraper_agent import ScraperAgent
from src.utils import save_data_to_csv, save_data_to_json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    # Optional: python main.py configs/other_site.json
    config_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BASE_DIR, "configs", "example_site_config.json")
    json_path = os.path.join(BASE_DIR, "data", "scraped_products.json")
    csv_path = os.path.join(BASE_DIR, "data", "scraped_products.csv")

    # 1. Load and validate the plan
    config = ConfigParser(config_path).load_config()

    # 2. Run the agent (set headless=False to watch the browser)
    agent = ScraperAgent(config=config, browser="chrome", headless=False)
    results = agent.run()

    # 3. Save results
    save_data_to_json(results, json_path)
    save_data_to_csv(results, csv_path)
    print(f"Successfully scraped {len(results)} items and saved to {json_path} and {csv_path}")


if __name__ == "__main__":
    main()
