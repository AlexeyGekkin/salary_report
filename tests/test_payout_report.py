import pytest
from reports.payout_report import PayoutReport
from models.employee import EmployeeRecord


@pytest.fixture
def sample_data():
    return [
        EmployeeRecord("Alice", "IT", 40.0, 25.0),
        EmployeeRecord("Bob", "IT", 35.0, 30.0),
        EmployeeRecord("Eve", "HR", 38.0, 28.0),
    ]


def test_generate_report_structure(sample_data):
    report = PayoutReport().generate(sample_data)
    assert "IT" in report
    assert "HR" in report
    assert any("Alice" in line for line in report["IT"])
    assert any("Bob" in line for line in report["IT"])
    assert any("Eve" in line for line in report["HR"])


@pytest.mark.parametrize(
    "name, expected_amount",
    [("Alice", "$1000.00"), ("Bob", "$1050.00"), ("Eve", "$1064.00")],
)
def test_payout_values(sample_data, name, expected_amount):
    report = PayoutReport().generate(sample_data)
    all_lines = sum(report.values(), [])
    assert any(expected_amount in line and name in line for line in all_lines)


def test_totals_are_correct(sample_data):
    report = PayoutReport().generate(sample_data)

    # IT: Alice (40×25=1000) + Bob (35×30=1050) → 75 ч, $2050
    it_total_line = report["IT"][-1]
    assert "75.0" in it_total_line
    assert "$2050.00" in it_total_line

    # HR: Eve (38×28=1064) → 38 ч, $1064
    hr_total_line = report["HR"][-1]
    assert "38.0" in hr_total_line
    assert "$1064.00" in hr_total_line
