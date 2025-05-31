from collections import defaultdict
from models.employee import EmployeeRecord


class PayoutReport:
    def generate(self, records: list[EmployeeRecord]) -> dict[str, list[str]]:
        header = (
            f"{' ':14}" f"{'name':<20}" f"{'hours':<7}" f"{'rate':<7}" f"{'payout':<7}"
        )

        report = defaultdict(list)

        for record in records:
            dept = record.department
            if not report[dept]:
                report[dept].append(header)

            payout = record.hours * record.rate
            report[dept].append(
                f"{'-' * 14}"
                f"{record.name:<20}"
                f"{record.hours:<7.1f}"
                f"{record.rate:<7.1f}"
                f"${payout:<7.2f}"
            )

            # Вставляем итого в конец прямо во время обхода
            if "_totals" not in report:
                report["_totals"] = {}
            if dept not in report["_totals"]:
                report["_totals"][dept] = {"hours": 0.0, "payout": 0.0}

            report["_totals"][dept]["hours"] += record.hours
            report["_totals"][dept]["payout"] += payout

        # Добавим строку с итогами
        for dept, lines in report.items():
            if dept == "_totals":
                continue
            totals = report["_totals"][dept]
            lines.append(
                f"{' ' * 34}" f"{totals['hours']:<14.1f}" f"${totals['payout']:<7.2f}"
            )

        report.pop("_totals")
        return dict(report)
