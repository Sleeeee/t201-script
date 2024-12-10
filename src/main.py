import argparse
from datagen import DataGen
from fetcher import Fetcher
from utils import Utils

VALID_OPERATORS = ["==", "!=", "<", ">", "<=", ">="]
COLUMNS_NAMES = ["Product ID", "Company", "Origin", "Category", "Stock", "Unit Price"]

def main():
    datagen, fetcher, utils = DataGen(), Fetcher(), Utils()

    parser = argparse.ArgumentParser(description="Manage and query product data")
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate_parser = subparsers.add_parser("generate", help="Generate JSON data files")
    generate_parser.add_argument("-f", "--files", type=int, default=10, help="Number of files (default: 10)")
    generate_parser.add_argument("-r", "--rows", type=int, default=200, help="Number of rows per file (default: 200)")

    subparsers.add_parser("delete", help="Delete all product data")

    fetch_parser = subparsers.add_parser("fetch", help="Fetch and sort data")
    fetch_parser.add_argument("-f", "--filter", action="append", nargs=3, metavar=("KEY", "OPERATOR", "VALUE"), help="Filter data by a specific key, logic operator and value")
    fetch_parser.add_argument("-s", "--sort", choices=COLUMNS_NAMES, help="Field to sort data by")
    fetch_parser.add_argument("-r", "--reverse", action="store_true", help="Sort data in descending order")
    fetch_parser.add_argument("-c", "--column", action="append", choices=COLUMNS_NAMES, help="Columns to fetch, default: all")

    args = parser.parse_args()

    if args.command == "generate":
        if utils.validate_input(f"Do you want to generate {args.files} files of {args.rows} each ?"):
            datagen.generate_data(args.files, args.rows)
            print("[t201-script] Data generated successfully")
        else:
            print("[t201-script] Data generation aborted")

    elif args.command == "delete":
        if utils.validate_input(f"Are you sure you want to delete all data files ?"):
            datagen.delete_data()
            print("[t201-script] Data deleted successfully")

    elif args.command == "fetch":
        filters = []
        if args.filter:
            for filter_args in args.filter:
                key, op, value = filter_args
                filters.append((key, op, value))
        sort = args.sort
        reverse = args.reverse
        columns = [column for column in args.column] if args.column else None

        fetch_description = "[t201-script] Are you sure you want to fetch"
        if columns:
            fetch_description += f" columns {', '.join(columns)}"
        else:
            fetch_description += " all columns"
        if filters:
            filter_desc = ", ".join([f"{key} {op} {value}" for key, op, value in filters])
            fetch_description += f" with filters ({filter_desc})"
        if sort:
            fetch_description += f" sorted by '{sort}'"
            fetch_description += f" in {"descending" if reverse else "ascending"} order"
        fetch_description += " ?"

        if not utils.validate_input(fetch_description):
            print("[t201-script] Data fetching aborted")
            return
        data = fetcher.fetch_data(filters, sort, reverse, columns)
        for row in data:
            print(row)
        analytics = fetcher.get_analytics(data)
        print(analytics)
        print("[t201-script] Data fetched successfully")
        if not utils.validate_input("Do you wish to export this data ?"):
            print("[t201-script] Data was not exported")
            return
        if not utils.validate_input("Do you want to include analytics ?"):
            content = [data]
        else:
            content = [data, analytics]
        fetcher.export_data(content)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[t201-script] Data processing cancelled by user input")
