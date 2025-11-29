
"""Pantry Pal — a tiny pantry tracker (Beginner-friendly)
(c) 2025 Shawniece Barrett. All Rights Reserved.
"""
import argparse
import json
from typing import Dict, Tuple, List

DEFAULT_PATH = "pantry.json"

# ---------------- core functions (top-level as required) ----------------
def load_pantry(path: str = DEFAULT_PATH) -> Dict[str, Dict[str, float]]:
    """Load pantry data from JSON; return empty structure if missing."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_pantry(pantry: Dict[str, Dict[str, float]], path: str = DEFAULT_PATH) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(pantry, f, indent=2, ensure_ascii=False)

def add_item(pantry: Dict[str, Dict[str, float]], name: str, qty: float, unit: str, min_qty: float = 0) -> Dict[str, Dict[str, float]]:
    """Add or increase an item. Returns the mutated pantry (for convenience)."""
    if qty < 0 or min_qty < 0:
        raise ValueError("Quantities must be non-negative")
    item = pantry.get(name.lower(), {"qty": 0.0, "unit": unit, "min": float(min_qty)})
    item["qty"] = float(item.get("qty", 0)) + float(qty)
    item["unit"] = unit
    item["min"] = max(float(item.get("min", 0)), float(min_qty))
    pantry[name.lower()] = item
    return pantry

def use_item(pantry: Dict[str, Dict[str, float]], name: str, qty: float) -> Dict[str, Dict[str, float]]:
    """Decrease an item's quantity; error if not enough."""
    key = name.lower()
    if key not in pantry:
        raise KeyError(f"Item '{name}' not found")
    if qty < 0:
        raise ValueError("qty must be non-negative")
    if pantry[key]["qty"] < qty:
        raise ValueError(f"Not enough '{name}' to use {qty} {pantry[key]['unit']}. Have {pantry[key]['qty']}.")
    pantry[key]["qty"] -= float(qty)
    return pantry

def low_stock(pantry: Dict[str, Dict[str, float]]) -> List[Tuple[str, float, float]]:
    """Return items where qty < min threshold: list of (name, qty, min)."""
    return sorted(
        [(name, data.get("qty", 0.0), data.get("min", 0.0)) for name, data in pantry.items() if data.get("qty", 0.0) < data.get("min", 0.0)],
        key=lambda x: x[0],
    )

# ---------------- interactive menu ----------------
def _input_float(prompt: str) -> float:
    while True:
        raw = input(prompt).strip()
        try:
            return float(raw)
        except ValueError:
            print("Please enter a number (e.g., 100 or 0.5).")

def interactive_menu(path: str = DEFAULT_PATH) -> None:
    print("Welcome to Pantry Pal!")
    while True:
        print("\nWhat would you like to do?")
        print("  1) Add an item")
        print("  2) Use an item")
        print("  3) List all items")
        print("  4) Show low stock")
        print("  5) Exit")
        choice = input("Enter choice (1-5): ").strip()

        pantry = load_pantry(path)

        if choice == "1":
            name = input("Item name: ").strip()
            qty = _input_float("Quantity to add: ")
            unit = input("Unit (e.g., g, kg, ml, L, pcs): ").strip()
            min_qty = _input_float("Minimum to keep on hand (0 to skip): ")
            try:
                add_item(pantry, name, qty, unit, min_qty)
                save_pantry(pantry, path)  # auto-save
                print(f"Added {qty} {unit} of {name}. Min={min_qty}")
            except ValueError as e:
                print(e)

        elif choice == "2":
            name = input("Item name: ").strip()
            qty = _input_float("Quantity to use: ")
            try:
                use_item(pantry, name, qty)
                save_pantry(pantry, path)  # auto-save
                print(f"Used {qty} of {name}.")
            except (KeyError, ValueError) as e:
                print(e)

        elif choice == "3":
            if not pantry:
                print("Pantry is empty.")
            else:
                for name, d in sorted(pantry.items()):
                    print(f"{name}: {d.get('qty',0)} {d.get('unit','')} (min {d.get('min',0)})")

        elif choice == "4":
            flags = low_stock(pantry)
            if not flags:
                print("No low-stock items. You're stocked!")
            else:
                print("Low-stock items:")
                for name, q, m in flags:
                    need = max(0.0, m - q)
                    print(f"- {name}: {q} / min {m} → need ~{need}")

        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Please choose 1-5.")

# ---------------- CLI ----------------
def main() -> None:
    parser = argparse.ArgumentParser(description="Pantry Pal — track what you have and what’s low")
    parser.add_argument("--path", default=DEFAULT_PATH, help="Path to pantry JSON (default: pantry.json)")
    sub = parser.add_subparsers(dest="cmd", required=False)  # allow interactive fallback

    p_add = sub.add_parser("add", help="Add or increase an item")
    p_add.add_argument("name")
    p_add.add_argument("qty", type=float)
    p_add.add_argument("unit", help="e.g., g, kg, ml, L, pcs")
    p_add.add_argument("--min", type=float, default=0, dest="min_qty", help="Low-stock threshold")

    p_use = sub.add_parser("use", help="Use some quantity of an item")
    p_use.add_argument("name")
    p_use.add_argument("qty", type=float)

    sub.add_parser("list", help="List all items")
    sub.add_parser("low", help="Show items below their minimum")

    args = parser.parse_args()

    # If no command provided, open the interactive menu
    if not args.cmd:
        interactive_menu(args.path)
        return

    pantry = load_pantry(args.path)

    if args.cmd == "add":
        add_item(pantry, args.name, args.qty, args.unit, args.min_qty)
        save_pantry(pantry, args.path)
        print(f"Added {args.qty} {args.unit} of {args.name}. Min={args.min_qty}")
    elif args.cmd == "use":
        try:
            use_item(pantry, args.name, args.qty)
            save_pantry(pantry, args.path)
            print(f"Used {args.qty} of {args.name}.")
        except (KeyError, ValueError) as e:
            print(e)
    elif args.cmd == "list":
        if not pantry:
            print("Pantry is empty.")
        else:
            for name, d in sorted(pantry.items()):
                print(f"{name}: {d.get('qty',0)} {d.get('unit','')} (min {d.get('min',0)})")
    elif args.cmd == "low":
        flags = low_stock(pantry)
        if not flags:
            print("No low-stock items. You're stocked!")
        else:
            print("Low-stock items:")
            for name, q, m in flags:
                need = max(0.0, m - q)
                print(f"- {name}: {q} / min {m} → need ~{need}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
