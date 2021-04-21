# -*- coding: utf-8 -*-
from sales.models import Product


class ProductService:
    @classmethod
    def get_product_name_map(cls):
        products = Product.objects.all()
        data = {
            product.name: product
            for product in products
        }
        return data
