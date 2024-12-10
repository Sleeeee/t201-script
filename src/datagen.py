import os
import random
from faker import Faker

class DataGen:
    def __init__(self):
        """
        PRE : None
        POST :
                - ~/.t201-script exists and is contained in self.directory
                - self.fake is a Faker object (used to create fake data)
                - the seed for random and Faker is 717
                - self.suppliers contains a list of fake company names
                - self.origins contains a list of arbitrary countries
                - self.categories contains a list of arbitrary words
        """
        self.directory = os.path.expanduser(f"~/.t201-script")
        os.makedirs(self.directory, exist_ok=True)

        self.fake = Faker()
        Faker.seed(717)
        random.seed(717)
        self.suppliers = self.fake_companies()
        self.origins = self.fake_countries()
        self.categories = self.fake_words()

    def fake_cities(self, n: int) -> list:
        """
        Generates a list of fake city names
        PRE : None
        POST : Returns a list containing n fake city names
        """
        if n <= 0:
            raise ValueError(f"n={n} must be > 0")
        # Only returning last word to avoid 'South', 'New', ... and ensuring unique city names (for simplicity naming product ids)
        return [self.fake.city().split(" ")[-1] for _ in range(n)]

    def fake_companies(self, n: int=30) -> list:
        """
        Generates a list of fake company names
        PRE : None
        POST : Returns a list containing n fake company names
        """
        if n <= 0:
            raise ValueError(f"n={n} must be > 0")
        # Replace avoids commas causing errors in CSV output
        return [self.fake.company().replace(",", "") for _ in range(n)]

    def fake_countries(self, n: int=50) -> list:
        """
        Generates a list of random country names
        PRE : None
        POST : Returns a list containing n arbitrary country names
        """
        if n <= 0:
            raise ValueError(f"n={n} must be > 0")
        return [self.fake.country() for _ in range(n)]

    def fake_words(self, n: int=50):
        """
        Generates a list of random words
        PRE : None
        POST : Returns a list containing n arbitrary words
        """
        if n <= 0:
            raise ValueError(f"n={n} must be > 0")
        return [self.fake.word().capitalize() for _ in range(n)]

    def generate_data(self, files: int, rows: int) -> None:
        """
        Generates [files] files with [rows] rows of data each
        PRE : self.directory exists / self.suppliers, self.origins, self.categories contain at least one item
        POST : self.directory contains [files] files named after departments (self.fake_cities), containing [rows] rows of data each. Each row of data picks a random item from self.suppliers, self.origins, self.categories
        """
        departments = self.fake_cities(files)
        for department in departments:
            content = "Product ID,Company,Origin,Category,Stock,Unit Price"
            for i in range(1, rows + 1):
                product_id = f"{department[:3].upper()}-{i:03}"
                company = random.choice(self.suppliers)
                origin = random.choice(self.origins)
                category = random.choice(self.categories)
                stock = str(random.randint(0, 999))
                unit_price = str(random.randint(0, 9999) / 100)
                line = ",".join([product_id, company, origin, category, stock, unit_price])
                content += f"\n{line}"
            try:
                with open(os.path.join(self.directory, f"{department}.csv"), "w") as file:
                    file.write(content)
                    print(f"Wrote to file {department}.csv")
            except Exception as e:
                print(f"Failed writing to file {department}.csv : {e}")

    def delete_data(self):
        """
        Delete all data from self.directory
        PRE : self.directory is an existing directory
        POST : self.directory does not contain any files (anymore)
        """
        for file in os.listdir(self.directory):
            os.remove(os.path.join(self.directory, file))
            print("Removed file {}".format(file))
