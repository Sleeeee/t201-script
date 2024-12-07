import argparse
from datagen import DataGen
from fetcher import Fetcher

def main():
    parser = argparse.ArgumentParser(description="Manage and query product data.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate_parser = subparsers.add_parser("generate", help="Generate JSON data files.")
    generate_parser.set_defaults(func=DataGen().generate_data)

    # Fetch data command
    fetch_parser = subparsers.add_parser("fetch", help="Fetch and sort data.")
    #fetch_parser.add_argument("-s", "--sort-by", help="Field to sort data by.")
    #fetch_parser.add_argument("-r", "--reverse", action="store_true", help="Sort in descending order.")
    fetch_parser.set_defaults(func=Fetcher().fetch_data)

    args = parser.parse_args()
    args.func()

if __name__ == "__main__":
    main()
