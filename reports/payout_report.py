class PayoutReport:
    def generate(self, rows: list[dict]) -> list[str]:
        report_lines = [f"{' ':14}{'name':<20}{'hours':<7}{'rate':<7}${'payout':<7}"]
        departments = {}

        for row in rows:
            department = row["department"]
            if department not in departments:
                departments[department] = []
            departments[department].append(row)
        print(departments)
        for department, employees in departments.items():
            report_lines.append(
                f"{department}"
            )
            total = 0
            for emp in employees:
                payout = emp["hours"] * emp["rate"]
                total += payout
                report_lines.append(
                    f"{'-' * 14}{emp['name']:<20}{emp['hours']:<7}{emp['rate']:<7}${payout:<7}"
                )
            report_lines.append(f"{' ' * 34}${total}")
            report_lines.append("")

        return report_lines