import csv
import os

class Fetcher:
    def __init__(self):
        self.directory = os.path.expanduser("~/.t201-script")
        self.headers = ["Product ID", "Company", "Origin", "Category", "Stock", "Unit Price"]

    def fetch_data(self, filters, sort, reverse):
        data = []
        for filename in os.listdir(self.directory):
            try:
                with open(os.path.join(self.directory, filename), "r") as f:
                    reader = csv.DictReader(f)
                    for line in reader:
                        if filters:
                            matches = all(line.get(key) == value for key, value in filters.items())
                            if matches:
                                data.append(line)
                        else:
                            data.append(line)
            except Exception as e:
                print(f"Error processing file {filename} : {e}")
        if sort:
            data.sort(key=lambda d: d[sort], reverse=reverse)
        return data
