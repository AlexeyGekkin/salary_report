from reports.payout_report import PayoutReport

def test_payout_report_generation():
    rows = [
        {'name': 'Alice', 'department': 'IT', 'hours': 40.0, 'rate': 25.0},
        {'name': 'Bob', 'department': 'IT', 'hours': 35.0, 'rate': 30.0},
        {'name': 'Eve', 'department': 'HR', 'hours': 38.0, 'rate': 28.0},
    ]

    report = PayoutReport().generate(rows)

    assert any("Alice" in line for line in report)
    assert any("Bob" in line for line in report)
    assert any("Eve" in line for line in report)
    assert any("IT" in line for line in report)
    assert any("HR" in line for line in report)
    assert any("$1000.0" in line for line in report)  # Alice
    assert any("$1050.0" in line for line in report)  # Bob
    assert any("$1064.0" in line for line in report)  # Eve