from database.db_config import get_db_connection, close_db_connection
import logging

logger = logging.getLogger(__name__)

class Product:
    def __init__(self, product_id, name, price):
        self.product_id = product_id
        self.name = name
        self.price = price

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "price": self.price
        }

    @staticmethod
    def get_all_products():
        logger.info("Fetching all products from the database")
        connection = get_db_connection()
        if not connection:
            raise Exception("Database connection failed")
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT id, name, price FROM products")
            products = cursor.fetchall()
            return [Product(product['id'], product['name'], product['price']) for product in products]
        finally:
            close_db_connection(connection)

    @staticmethod
    def get_product_by_id(product_id):
        logger.info(f"Fetching product with ID {product_id}")
        connection = get_db_connection()
        if not connection:
            raise Exception("Database connection failed")
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT id, name, price FROM products WHERE id = %s", (product_id,))
            product = cursor.fetchone()
            return Product(product['id'], product['name'], product['price']) if product else None
        finally:
            close_db_connection(connection)

    @staticmethod
    def create_product(name, price):
        if not name or not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("Invalid name or price")
        logger.info(f"Creating product: {name}, {price}")
        connection = get_db_connection()
        if not connection:
            raise Exception("Database connection failed")
        try:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO products (name, price) VALUES (%s, %s)", (name, price))
            connection.commit()
            return Product(cursor.lastrowid, name, price)
        except Exception as e:
            connection.rollback()
            logger.error("Error creating product", exc_info=True)
            raise e
        finally:
            close_db_connection(connection)

    @staticmethod
    def update_product(product_id, name=None, price=None):
        if not name and not price:
            raise ValueError("At least one field (name or price) is required")
        logger.info(f"Updating product {product_id}")
        connection = get_db_connection()
        if not connection:
            raise Exception("Database connection failed")
        try:
            updates = []
            params = []
            if name:
                updates.append("name = %s")
                params.append(name)
            if price:
                if not isinstance(price, (int, float)) or price <= 0:
                    raise ValueError("Price must be a positive number")
                updates.append("price = %s")
                params.append(price)
            params.append(product_id)
            query = f"UPDATE products SET {', '.join(updates)} WHERE id = %s"
            cursor = connection.cursor()
            cursor.execute(query, tuple(params))
            connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            connection.rollback()
            logger.error("Error updating product", exc_info=True)
            raise e
        finally:
            close_db_connection(connection)

    @staticmethod
    def delete_product(product_id):
        logger.info(f"Deleting product with ID {product_id}")
        connection = get_db_connection()
        if not connection:
            raise Exception("Database connection failed")
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
            connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            connection.rollback()
            logger.error("Error deleting product", exc_info=True)
            raise e
        finally:
            close_db_connection(connection)
