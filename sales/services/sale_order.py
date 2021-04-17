# -*- coding: utf-8 -*-
from django.db.models import Sum, Max

from sales.models import SaleOrder


class SaleOrderService:
    @staticmethod
    def _get_average_sales(sale_orders):
        annotation = sale_orders.aggregate(
            total_revenue=Sum('revenue'),
            total_sales_number=Sum('sales_number')
        )
        return annotation['total_revenue'] / annotation['total_sales_number']

    def get_average_sales_by_user(self, user, sale_orders):
        return self._get_average_sales(sale_orders.filter(user=user))

    def get_average_sales_by_all_users(self, sale_orders):
        return self._get_average_sales(sale_orders)

    @staticmethod
    def get_highest_sale_revenue_for_user(user, sale_orders):
        sale_order = sale_orders.filter(user=user).order_by('-revenue').first()
        return {
            'product_name': sale_order.product.name,
            'price': sale_order.revenue
        }

    @staticmethod
    def get_highest_sale_number_for_user(user, sale_orders):
        sale_order = sale_orders.filter(user=user).order_by('-sale_number').first()
        return {
            'product_name': sale_order.product.name,
            'price': sale_order.revenue
        }

    def get_statistic_by_user(self, user):
        sale_orders = SaleOrder.objects.all().select_related('product', 'user')
        average_sales_for_current_user = self.get_average_sales_by_user(user, sale_orders)
        average_sales_for_all_users = self.get_average_sales_by_all_users(sale_orders)
        product_highest_revenue_for_current_user = self.get_highest_sale_revenue_for_user(user, sale_orders)
        product_highest_sales_number_for_current_user = self.get_highest_sale_revenue_for_user(user, sale_orders)
        return {
            'average_sales_for_current_user': average_sales_for_current_user,
            'average_sales_for_all_users': average_sales_for_all_users,
            'product_highest_revenue_for_current_user': product_highest_revenue_for_current_user,
            'product_highest_sales_number_for_current_user': product_highest_sales_number_for_current_user
        }
