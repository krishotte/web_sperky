"""Product Model."""

from config.database import Model
from orator.orm import belongs_to, belongs_to_many, has_many


class Product(Model):
    """Product Model."""
    __fillable__ = ['name', 'category_id', 'price', 'description', 'image_folder', 'detail', 'note']

    @belongs_to('category_id', 'id')
    def category(self):
        from app.Product_category import Product_category
        return Product_category

    @belongs_to_many()
    def materials(self):
        from app.Material import Material
        return Material

    @belongs_to_many('products_related', 'product_id', 'related_id')
    # this somehow magically works - stores Product.id into product_id and related_products[Product].id into related_id
    def related_products(self):
        # referenced products
        from app.Product import Product
        return Product

    @belongs_to_many
    def orders(self):
        from app.Order import Order
        return Order

    @belongs_to
    def availability(self):
        from app.Availability import Availability
        return Availability

    @has_many
    def variants(self):
        from app.Variant import Variant
        return Variant.order_by('id')
