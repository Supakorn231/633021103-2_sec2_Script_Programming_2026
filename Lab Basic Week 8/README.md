# Week 8: Automating with CSV and JSON Data

## Requirements
- Python 3.8 or later
- No third-party packages are required (`csv` and `json` are built into Python).

## Run
Open a terminal in the `week8-data-processor` folder and run:

```bash
python main.py
```

The script reads `data/input_sales.csv` and `data/input_inventory.json`, then creates:
- `data/output_filtered_sales.csv`
- `data/output_updated_inventory.json`

CSV rows are filtered where `Amount >= 100`. The summary row includes total sales, average item price, and filtered row count. JSON stock is updated for `PROD001` and `PROD003`, and product `PROD004` is added.
