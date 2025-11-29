# Pantry Pal

Pantry Pal is a beginner-friendly command-line program that helps users track ingredient quantities, units, and low-stock thresholds. This project was created for the CS50 final project.

## Overview

Pantry Pal allows users to:
- Add items to a pantry list
- Use (subtract) quantities from existing items
- View all stored items
- Display low-stock alerts based on minimum thresholds
- Automatically save data to a JSON file
- Use either the interactive menu or command-line arguments

## How to Run

### Interactive Menu Mode
```
python pantrypal.py
```

### Command-Line Usage
```
python pantrypal.py add ITEM_NAME QTY UNIT --min MINIMUM
python pantrypal.py use ITEM_NAME QTY
python pantrypal.py list
python pantrypal.py low
```

Example:
```
python pantrypal.py add rice 2 kg --min 1
python pantrypal.py use rice 0.5
```

## File Descriptions

- `pantrypal.py` — Main program file  
- `pantry.json` — Data file created automatically on first run  
- `README.md` — Project documentation

## Design Notes

- All pantry items are stored as dictionaries inside a main pantry dictionary.
- Data is saved to and loaded from `pantry.json` using JSON formatting.
- The program uses functions like `add_item`, `use_item`, and `low_stock` to keep logic organized.
- The command-line interface is built with Python's `argparse` module.
- If no command-line arguments are provided, the program launches the interactive menu.

## Video Demonstration

Insert video link here.

## Author

Shawniece Barrett
