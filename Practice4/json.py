"""
json.py
Practice 4 — JSON
"""

from __future__ import annotations
import json
from pathlib import Path
from typing import Any


def parse_json_string() -> None:
    json_text = '{"name": "Sanzhar", "age": 18, "skills": ["python", "git"], "active": true}'
    data = json.loads(json_text)  # str -> dict
    print("Parsed from string:", data)
    print("Name:", data["name"])
    print()


def python_to_json_string() -> None:
    obj = {
        "course": "Practice 4",
        "topics": ["iterators", "dates", "math", "json"],
        "passed": True,
        "score": 100,
    }
    s = json.dumps(obj, indent=2, ensure_ascii=False)  
    print("Dump to JSON string:\n", s)
    print()


def write_json_file(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def read_json_file(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def work_with_sample_data(sample_path: Path) -> None:
    if not sample_path.exists():
        demo_sample = {
            "students": [
                {"id": 1, "name": "Aruzhan", "gpa": 3.4},
                {"id": 2, "name": "Dias", "gpa": 2.9},
                {"id": 3, "name": "Amina", "gpa": 3.8},
            ]
        }
        write_json_file(sample_path, demo_sample)
        print(f"sample-data.json not found, created demo at: {sample_path}")

    data = read_json_file(sample_path)
    print("Loaded sample-data.json:", data)

    students = data.get("students", [])
    print("Students count:", len(students))

    strong = [s for s in students if float(s.get("gpa", 0)) >= 3.0]
    print("GPA >= 3.0:", [s.get("name") for s in strong])

    out_path = sample_path.parent / "sample-data-processed.json"
    write_json_file(out_path, {"strong_students": strong})
    print("Wrote processed JSON to:", out_path)
    print()


def main() -> None:
    parse_json_string()
    python_to_json_string()

    out = Path("example.json")
    write_json_file(out, {"hello": "world", "n": 123})
    print("Wrote example.json")

    loaded = read_json_file(out)
    print("Read example.json:", loaded)
    print()

    work_with_sample_data(Path("sample-data.json"))


if __name__ == "__main__":
    main()