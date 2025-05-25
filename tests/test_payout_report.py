from reports.payout_report import PayoutReport


def test_payout_report_generation():
    rows = [
        {'name': 'Alice', 'department': 'IT', 'hours': 40.0, 'rate': 25.0},
        {'name': 'Bob', 'department': 'IT', 'hours': 35.0, 'rate': 30.0},
        {'name': 'Eve', 'department': 'HR', 'hours': 38.0, 'rate': 28.0},
    ]

    report = PayoutReport().generate(rows)

    assert "IT" in report
    assert "HR" in report

    all_lines = []
    for lines in report.values():
        all_lines.extend(lines)

    # Проверка присутствия имён
    assert any("Alice" in line for line in all_lines)
    assert any("Bob" in line for line in all_lines)
    assert any("Eve" in line for line in all_lines)

    # Проверка корректных выплат
    assert any("$1000.0" in line for line in all_lines)  # 40 * 25
    assert any("$1050.0" in line for line in all_lines)  # 35 * 30
    assert any("$1064.0" in line for line in all_lines)  # 38 * 28

    # Проверка итогов по отделу IT
    it_totals = [line for line in report["IT"] if "$" in line][-1]
    assert "75.0" in it_totals  # Сумма часов: 40 + 35
    assert "$2050.0" in it_totals  # Выплата: 1000 + 1050

    # Проверка итогов по отделу HR
    hr_totals = [line for line in report["HR"] if "$" in line][-1]
    assert "38.0" in hr_totals
    assert "$1064.0" in hr_totals
