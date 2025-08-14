import json
from argparse import ArgumentParser

from tabulate import tabulate

from loganalyzer.filters import (
    create_date_filter,
    create_user_agent_filter,
    validate_date,
)
from loganalyzer.reader import load_json_data, load_log_data
from loganalyzer.reports import AverageTimeReport, ReportManager, UserAgentReport

reports_types = {"average": AverageTimeReport, "user_agent": UserAgentReport}


def main():
    """Main CLI App."""
    parser = ArgumentParser(description="Python Log Analyzer")
    parser.add_argument(
        "--file",
        type=str,
        nargs="+",
        default=2,
        help="provide a file(s) for analyze",
        required=True,
    )
    parser.add_argument(
        "--report", type=str, default=2, help="provide a report type", required=True
    )
    parser.add_argument(
        "--date", type=str, default=None, help="provide a date filter (%%Y-%%m-%%d)"
    )
    parser.add_argument(
        "--user-agent", type=str, default=None, help="provide a user agent filter"
    )
    parser.add_argument(
        "--fileformat",
        type=str,
        default="log",
        help="provide a fileformat (log or json)",
    )

    args = parser.parse_args()

    files = args.file
    data = []
    filters = []

    load_method = load_log_data if args.fileformat == "log" else load_json_data

    try:
        for file in files:
            data += load_method(file)
    except (FileNotFoundError, PermissionError, json.decoder.JSONDecodeError) as ex:
        print(f"Fatal error when opening {file}: {ex}")
        return

    if args.date:
        validate_date(args.date)

        filters.append(create_date_filter(args.date))

    if args.user_agent:
        filters.append(create_user_agent_filter(args.user_agent))

    report_type = reports_types.get(args.report)

    if report_type is None:
        print(f"Fatal error: {args.report} report type not supported.")
        return

    report_manager = ReportManager(report_type, data, filters)
    report = report_manager.generate()

    print(tabulate(report, showindex="always", headers="keys"))


if __name__ == "__main__":
    main()
