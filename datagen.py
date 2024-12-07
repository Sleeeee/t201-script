import os
import random
from faker import Faker

class DataGen:
    def __init__(self):
        self.fake = Faker()
        Faker.seed(717)
        random.seed(717)
        self.departments = self.fake_cities() # product ids start with uppercase first three letters
        self.suppliers = self.fake_companies()
        self.origins = self.fake_countries()
        self.categories = self.fake_categories()

    def fake_cities(self, n=10):
        """Generate a list of random city names."""
        return [self.fake.city().split(" ")[-1] for _ in range(n)]

    def fake_companies(self, n=30):
        """Generate a list of random company names."""
        return [self.fake.company() for _ in range(n)]

    def fake_countries(self, n=50):
        """Generate a list of random country names."""
        return [self.fake.country() for _ in range(n)]

    def fake_categories(self, n=50):
        """Generate a list of random brand names."""
        return [self.fake.word().capitalize() for _ in range(n)]

    def generate_data(self, rows=200):
        for department in self.departments:
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
            directory = os.path.expanduser(f"~/.t201-script")
            os.makedirs(directory, exist_ok=True)
            with open(os.path.join(directory, f"{department}.csv"), "w") as file:
                file.write(content)
                print(f"Wrote to file {department}.csv")
