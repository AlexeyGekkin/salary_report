class PayoutReport:
    def generate(self, rows: list[dict]) -> dict[str, list[str]]:
        header = (
            f"{' ':14}"
            f"{'name':<20}"
            f"{'hours':<7}"
            f"{'rate':<7}"
            f"{'payout':<7}"
        )

        report = {}

        for row in rows:
            dept = row["department"]
            if dept not in report:
                report[dept] = [header]
            hours = float(row["hours"])
            rate = float(row["rate"])
            payout = hours * rate
            report[dept].append(
                f"{'-' * 14}"
                f"{row['name']:<20}"
                f"{hours:<7.1f}"
                f"{rate:<7.1f}"
                f"${payout:<7.2f}"
            )

        for dept, lines in report.items():
            total_hours = sum(float(r["hours"]) for r in rows if r["department"] == dept)
            total_payout = sum(float(r["hours"]) * float(r["rate"]) for r in rows if r["department"] == dept)
            lines.append(
                f"{' ' * 34}{total_hours:<14.1f}${total_payout:<7.2f}"
            )

        return report
