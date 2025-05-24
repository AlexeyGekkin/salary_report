COLUMN_NAMES = {
    'name': ['name', 'Name'],
    'department': ['department', 'Dep', 'dep', 'Department'],
    'hours': ['hours', 'hours_worked', 'Hour'],
    'rate': ['rate', 'Rate', 'hourly_rate', 'salary']
}


def normalize_headers(headers: list[str]) -> dict[str, int]:
    normalized = {}
    for i, h in enumerate(headers):
        h_clean = h.strip().lower()
        for key, names in COLUMN_NAMES.items():
            if h_clean in names:
                normalized[key] = i
                break
    return normalized


def read_csv(path: str) -> list[dict]:
    rows = []
    with open(path, encoding='utf-8') as f:
        lines = [line for line in f if line.strip()]

    if not lines:
        return []

    headers = normalize_headers(lines[0].strip().split(','))

    for line in lines[1:]:
        parts = line.strip().split(',')
        if len(parts) < len(headers):
            continue

        row = {}
        for key, index in headers.items():
            value = parts[index].strip()
            if key in ['hours', 'rate']:
                try:
                    value = float(value)
                except ValueError:
                    raise ValueError(
                        f"Невозможно преобразовать '{value}'"
                        f" в число (поле '{key}')."
                    )
            row[key] = value

        rows.append(row)
    return rows
