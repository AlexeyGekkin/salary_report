import sys
import tempfile
from main import main


def test_main_output(monkeypatch, capsys):
    csv_data = "name,department,hours,rate\nAlice,HR,40,30"

    with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False
    ) as f:
        f.write(csv_data)
        temp_path = f.name

    # подменяем sys.argv
    monkeypatch.setattr(
        sys,
        "argv",
        ["main.py", temp_path, "--report", "payout"]
    )
    main()

    captured = capsys.readouterr()
    assert "Alice" in captured.out
    assert "HR" in captured.out
    assert "$1200.0" in captured.out
