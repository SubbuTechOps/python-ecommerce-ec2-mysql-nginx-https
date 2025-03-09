# backend/routes/__init__.py

# This file marks the routes directory as a package.
# You can optionally initialize imports for all blueprints here.

from .auth_routes import auth_bp
from .product_routes import product_bp
from .cart_routes import cart_bp
from .order_routes import order_bp
