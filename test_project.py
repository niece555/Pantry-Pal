
# Tests for Pantry Pal (beginner-friendly)
import project

def test_add_and_accumulate():
    p = {}
    project.add_item(p, "Flour", 500, "g", min_qty=200)
    project.add_item(p, "Flour", 250, "g")  # accumulate
    assert p["flour"]["qty"] == 750
    assert p["flour"]["unit"] == "g"
    assert p["flour"]["min"] == 200

def test_use_item_and_errors():
    p = {"sugar": {"qty": 300, "unit": "g", "min": 100}}
    project.use_item(p, "sugar", 100)
    assert p["sugar"]["qty"] == 200
    import pytest
    with pytest.raises(ValueError):
        project.use_item(p, "sugar", 500)
    with pytest.raises(KeyError):
        project.use_item(p, "honey", 10)

def test_low_stock_detection():
    p = {
        "rice": {"qty": 0.5, "unit": "kg", "min": 1.0},
        "beans": {"qty": 2, "unit": "pcs", "min": 1},
        "oil": {"qty": 0.2, "unit": "L", "min": 0.5},
    }
    lows = project.low_stock(p)
    names = [n for n, *_ in lows]
    assert "rice" in names and "oil" in names and "beans" not in names
