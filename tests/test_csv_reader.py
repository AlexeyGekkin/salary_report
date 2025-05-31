import pytest
import tempfile
import os

from utils.csv_reader import read_csv, normalize_header, EmployeeRecord


@pytest.mark.parametrize(
    "input_header,expected",
    [
        ("name", "name"),
        ("full name", "name"),
        ("employee name", "name"),
        ("department", "department"),
        ("dep", "department"),
        ("division", "department"),
        ("hours", "hours"),
        ("hours_worked", "hours"),
        ("time", "hours"),
        ("rate", "rate"),
        ("hourly_rate", "rate"),
        ("payment", "rate"),
    ],
)
def test_normalize_header(input_header, expected):
    assert normalize_header(input_header) == expected


def test_read_csv_success():
    content = "full name,dep,hours_worked,payment\nBob,IT,40,20\nAlice,HR,38,25"
    with tempfile.NamedTemporaryFile(
        delete=False, mode="w", encoding="utf-8", suffix=".csv"
    ) as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    records = read_csv(tmp_path)
    os.remove(tmp_path)

    assert len(records) == 2
    assert isinstance(records[0], EmployeeRecord)
    assert records[0].name == "Bob"
    assert records[1].hours == 38.0


def test_read_csv_missing_fields():
    content = "full name,dep\nJohn,Sales"
    with tempfile.NamedTemporaryFile(
        delete=False, mode="w", encoding="utf-8", suffix=".csv"
    ) as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    with pytest.raises(ValueError, match="Missing required fields"):
        read_csv(tmp_path)
    os.remove(tmp_path)


def test_read_csv_invalid_numbers():
    content = "name,department,hours,rate\nJohn,Sales,abc,xyz"
    with tempfile.NamedTemporaryFile(
        delete=False, mode="w", encoding="utf-8", suffix=".csv"
    ) as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    with pytest.raises(ValueError, match="Invalid data format in line"):
        read_csv(tmp_path)
    os.remove(tmp_path)
