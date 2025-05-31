from models.employee import EmployeeRecord
from .constants import FIELD_ALIASES


def normalize_header(header: str) -> str:
    header = header.strip().lower()
    for standard, aliases in FIELD_ALIASES.items():
        if header in (alias.lower() for alias in aliases):
            return standard
    return ""


def read_csv(file_path: str) -> list[EmployeeRecord]:
    rows: list[EmployeeRecord] = []

    with open(file_path, encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    if not lines:
        raise ValueError("CSV file is empty.")

    raw_headers = lines[0].split(",")
    headers = [normalize_header(h) for h in raw_headers]

    required_fields = set(FIELD_ALIASES.keys())
    if not required_fields.issubset(set(headers)):
        raise ValueError(f"Missing required fields. Found headers: {headers}")

    for line in lines[1:]:
        values = line.split(",")
        if len(values) != len(headers):
            raise ValueError(f"Line has unexpected number of columns: {line}")

        data = dict(zip(headers, values))

        try:
            record = EmployeeRecord(
                name=data["name"],
                department=data["department"],
                hours=float(data["hours"]),
                rate=float(data["rate"]),
            )
        except KeyError as e:
            raise ValueError(f"Missing field {e.args[0]} in line: {line}")
        except ValueError as e:
            raise ValueError(f"Invalid data format in line: {line} → {e}")

        rows.append(record)

    return rows
