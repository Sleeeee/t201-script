import operator
import csv
import os

class Fetcher:
    OPERATORS = {"==": operator.eq, "!=": operator.ne, "<": operator.lt, ">": operator.gt, "<=": operator.le, ">=": operator.ge}

    def __init__(self):
        self.directory = os.path.expanduser("~/.t201-script")
        self.headers = ["Product ID", "Company", "Origin", "Category", "Stock", "Unit Price"]

    def fetch_data(self, filters: list, sort: list, reverse: bool) -> list:
        """
        Fetches data from CSV files contained in self.directory
        PRE : filters contains three items (key, operator, value) or is None / sort contains one item (key corresponding to a column header) or is None
        POST : Returns a list containing each CSV row matching the filters (all rows if filters is None), sorted by sort (not sorted if sort is None)
        """
        data = []
        for filename in os.listdir(self.directory):
            try:
                with open(os.path.join(self.directory, filename), "r") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if self.row_matches_filters(row, filters):
                            data.append(row)
            except Exception as e:
                print(f"Error processing file {filename} : {e}")
        if sort:
            data.sort(key=lambda d: d[sort], reverse=reverse)
        return data

    def row_matches_filters(self, row: dict, filters: list) -> bool:
        """
        PRE : row contains keys corresponding to column names
        POST : Returns True if row matches filters (or if filters is None) / False if not
        RAISES : ValueError if the operator (filters[1]) is not a valid operator (contained in self.OPERATORS)
        """
        if not filters:
            return True
        for key, op, value in filters:
            op_func = self.OPERATORS.get(op)
            if not op_func:
                raise ValueError(f"Invalid operator: {op}")

            row_value = row.get(key)
            try:
                # Parse numbers
                row_value = float(row_value)
                value = float(value)
            except ValueError:
                # Keep strings as strings
                pass

            if not op_func(row_value, value):
                return False
            return True
