# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import os
import sys
import csv
import django


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
django.setup()
from sales.models import Product


def add_products():
    with open(f'{BASE_DIR}/scripts/data/product.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            date, product, sales_number, revenue, user_id = row
            _, created = Product.objects.get_or_create(name=product)
            if created:
                print(f"Created product name {product}")


if __name__ == '__main__':
    add_products()
    print("Done")
