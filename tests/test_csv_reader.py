import tempfile
import os
from utils.csv_reader import read_csv


def test_read_csv_basic():
    content = "name,department,hours,rate\nJohn,IT,40,25\nJane Smith,HR,38,30"

    with tempfile.NamedTemporaryFile('w+', delete=False, suffix='.csv') as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    try:
        rows = read_csv(tmp_path)
        assert len(rows) == 2
        assert rows[0]['name'] == 'John Doe'
        assert rows[0]['department'] == 'IT'
        assert rows[0]['hours'] == 40.0
        assert rows[0]['rate'] == 25.0
    finally:
        os.remove(tmp_path)
