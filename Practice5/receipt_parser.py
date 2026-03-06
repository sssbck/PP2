import json
import re
from pathlib import Path
from typing import Any

def parse_receipt(text: str) -> dict[str, Any]:

    lines = [line.rstrip() for line in text.splitlines() if line.strip()]

    all_prices = [
        float(x) for x in re.findall(r"\b\d+\.\d{2}\b(?!\s*x)", text)
    ]

    date_time_match = re.search(
        r"\b(\d{2}[./-]\d{2}[./-]\d{4})\s+(\d{2}:\d{2}(?::\d{2})?)\b",
        text,
    )
    date = date_time_match.group(1) if date_time_match else None
    time = date_time_match.group(2) if date_time_match else None


    payment_match = re.search(
        r"(?im)^\s*payment\s*method\s*[:\-]?\s*([A-Z ]+)\s*$",
        text,
    )
    if not payment_match:
        payment_match = re.search(r"(?im)^\s*(CARD|CASH|QR|TRANSFER)\s*$", text)
    payment_method = payment_match.group(1).strip() if payment_match else None

    subtotal_match = re.search(r"(?im)^\s*subtotal\s+(-?\d+\.\d{2})\s*$", text)
    total_match = re.search(r"(?im)^\s*total\s+(-?\d+\.\d{2})\s*$", text)
    discount_match = re.search(
        r"(?im)^\s*discount\s+(-?\d+\.\d{2})-?\s*$", text
    )

    subtotal = float(subtotal_match.group(1)) if subtotal_match else None
    total = float(total_match.group(1)) if total_match else None
    discount = float(discount_match.group(1)) if discount_match else None

    item_pattern = re.compile(
        r"^(?P<name>[A-Za-zА-Яа-я0-9 %()\-/]+?)\s{2,}"
        r"(?P<qty>\d+(?:\.\d+)?)\s*x\s*"
        r"(?P<unit_price>\d+\.\d{2})\s+"
        r"(?P<line_total>\d+\.\d{2})$"
    )

    items = []
    for line in lines:
        match = item_pattern.match(line)
        if match:
            item = {
                "name": match.group("name").strip(),
                "quantity": float(match.group("qty")),
                "unit_price": float(match.group("unit_price")),
                "line_total": float(match.group("line_total")),
            }
            items.append(item)

    product_names = [item["name"] for item in items]
    calculated_total = round(sum(item["line_total"] for item in items), 2)

    return {
        "date": date,
        "time": time,
        "payment_method": payment_method,
        "product_names": product_names,
        "items": items,
        "all_prices": all_prices,
        "subtotal": subtotal,
        "discount": discount,
        "total": total,
        "calculated_total_from_items": calculated_total,
    }


def main() -> None:
    receipt_path = Path(__file__).with_name("raw.txt")
    text = receipt_path.read_text(encoding="utf-8")
    parsed = parse_receipt(text)

    print("Parsed receipt data:")
    print(json.dumps(parsed, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
