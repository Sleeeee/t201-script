import json
import operator
import csv
import os

class Fetcher:
    OPERATORS = {"==": operator.eq, "!=": operator.ne, "<": operator.lt, ">": operator.gt, "<=": operator.le, ">=": operator.ge}

    def __init__(self):
        self.directory = os.path.expanduser("~/.t201-script")

    @staticmethod
    def get_column_type(value):
        """
        Returns the type of the value given, categorized either number or text
        PRE : None
        POST : Returns float if value is a number, str if not
        """
        try:
            float(value)
            return float
        except ValueError:
            return str

    def fetch_data(self, filters: list, sort: list, reverse: bool, columns: list) -> list:
        """
        Fetches data from CSV files contained in self.directory
        PRE : filters contains three items (key, operator, value) or is None / sort contains one item (key corresponding to a column header) or is None
        POST : Returns a list containing each CSV row containing the specified columns, matching the filters (all rows if filters is None), sorted by sort (not sorted if sort is None)
        """
        data = []
        for filename in os.listdir(self.directory):
            try:
                with open(os.path.join(self.directory, filename), "r") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if self.row_matches_filters(row, filters):
                            if columns:
                                row = {key: row[key] for key in columns}
                            data.append(row)
            except Exception as e:
                print(f"Error processing file {filename} : {e}")
        if sort:
            if data:
                column_type = self.get_column_type(data[0][sort])
                data.sort(key=lambda d: column_type(d[sort]), reverse=reverse)
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

    @staticmethod
    def get_analytics(data: list) -> tuple:
        """
        Generate analytics from the input data
        PRE : data is a list of dictionaries containing valid column names
        POST :
        """
        numeric_stats = {}
        categorical_counts = {}

        for row in data:
            for key, value in row.items():
                try:
                    numeric_value = float(value)
                    if key not in numeric_stats:
                        numeric_stats[key] = {
                            "total": 0,
                            "max": numeric_value,
                            "min": numeric_value,
                            "count": 0
                        }
                    numeric_stats[key]["total"] += numeric_value
                    numeric_stats[key]["max"] = max(numeric_value, numeric_stats[key]["max"])
                    numeric_stats[key]["min"] = min(numeric_value, numeric_stats[key]["min"])
                    numeric_stats[key]["count"] += 1
                except ValueError:
                    # If the value is not numeric
                    if key not in categorical_counts:
                        categorical_counts[key] = {}
                    categorical_counts[key][value] = categorical_counts[key].get(value, 0) + 1

        for key, stats in numeric_stats.items():
            # Compute means once all the data is fetched
            stats["mean"] = stats["total"] / stats["count"]

        return numeric_stats, categorical_counts

    def export_data(self, content: list) -> None:
        """
        Export data into a JSON file in self.directory
        PRE : self.directory exists
        POST : output.json exists in self.directory, it contains the data given as parameter dumped to JSON
        """
        try:
            with open(os.path.join(self.directory, "output.json"), "w") as file:
                    file.write(f"{json.dumps(content)}\n")
        except Exception as e:
            print(f"Error processing file output.json : {e}")
