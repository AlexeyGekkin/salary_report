import argparse
import os
import sys
from typing import List

from utils.csv_reader import read_csv
from formats import FORMATTERS
from reports import REPORTS


def parse_args(args: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Формирование отчётов по зарплатам из CSV-файлов"
    )
    parser.add_argument(
        'files',
        nargs='*',
        help='Пути к CSV-файлам. Если не указаны — берутся все из папки data/'
    )
    parser.add_argument(
        '--report',
        required=True,
        help='Тип отчёта (например: payout)'
    )
    parser.add_argument(
        "--format",
        default="json",
        help="Формат вывода (json)")
    return parser.parse_args(args)


def main() -> None:
    args = parse_args(sys.argv[1:])
    files = args.files
    report_name = args.report
    output_format = args.format
    if not files:
        if not os.path.isdir('data'):
            print("Ошибка: папка 'data' не найдена и файлы не указаны.")
            sys.exit(1)

        files = [
            os.path.join('data', f)
            for f in os.listdir('data')
            if f.endswith('.csv')
        ]

    if not files:
        print("Ошибка: нет CSV-файлов для обработки.")
        sys.exit(1)

    if report_name not in REPORTS:
        print(f"Неизвестный тип отчёта: {report_name}")
        sys.exit(1)

    all_rows = []

    for file_path in files:
        if not os.path.exists(file_path):
            print(f"Ошибка: файл не найден: {file_path}")
            sys.exit(1)
        try:
            all_rows.extend(read_csv(file_path))
        except Exception as e:
            print(f"Ошибка чтения файла {file_path}: {e}")
            sys.exit(1)

    report = REPORTS[report_name].generate(all_rows)
    formatter = FORMATTERS[output_format]
    print(formatter.format(report))


if __name__ == "__main__":
    main()