from .auth import login
from .staff_dashboard import staff_dashboard
from .customer_dashboard import customer_dashboard
from .product_menu import product_menu
from .customer_menu import customer_menu
from .sale_menu import sale_menu
from .testing_menu import testing_menu

__all__ = [
    'login',
    'staff_dashboard',
    'customer_dashboard',
    'product_menu',
    'customer_menu',
    'sale_menu',
    'testing_menu'
]