import argparse
from datagen import DataGen
from fetcher import Fetcher
from utils import Utils

def main():
    datagen, utils = DataGen(), Utils()

    parser = argparse.ArgumentParser(description="Manage and query product data")
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate_parser = subparsers.add_parser("generate", help="Generate JSON data files")
    generate_parser.add_argument("-f", "--files", type=int, default=10, help="Number of files (default: 10)")
    generate_parser.add_argument("-r", "--rows", type=int, default=200, help="Number of rows per file (default: 200)")

    subparsers.add_parser("delete", help="Delete all product data")

    fetch_parser = subparsers.add_parser("fetch", help="Fetch and sort data")
    fetch_parser.add_argument("-f", "--filter", action="append", nargs=2, metavar=("KEY", "VALUE"), help="Filter data by a specific key and value")
    fetch_parser.add_argument("-s", "--sort", choices=["Product ID", "Company", "Origin", "Category", "Stock", "Unit Price"], help="Field to sort data by")
    fetch_parser.add_argument("-r", "--reverse", action="store_true", help="Sort data in descending order")

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
        filters = {key: value for key, value in args.filter} if args.filter else None
        sort = args.sort
        reverse = args.reverse
        fetch_description = "[t201-script] Are you sure you want all data"
        if filters:
            filter_desc = ", ".join([f"{key} = {value}" for key, value in filters.items()])
            fetch_description += f" with filters ({filter_desc})"
        if sort:
            fetch_description += f" sorted by '{sort}'"
            fetch_description += f" in {"descending" if reverse else "ascending"} order"
        fetch_description += " ?"
        if utils.validate_input(fetch_description):
            data = Fetcher().fetch_data(filters, sort, reverse)
            for row in data:
                print(row)
            print("[t201-script] Data fetched successfully")
        else:
            print("[t201-script] Data fetching aborted")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[t201-script] Data processing cancelled by user input")
