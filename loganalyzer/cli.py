from argparse import ArgumentParser


def main():
    """Main CLI App."""
    parser = ArgumentParser(description="Python Log Analyzer")
    parser.add_argument("--file", type=str, default=2, help="provide a file log")
    parser.add_argument("--report", type=str, default=2, help="provide a report type")
    parser.parse_args()
