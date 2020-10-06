from orator.migrations import Migration


class CreateOrdersProductsTable(Migration):
    # pivot table for many-to-many relationship of orders and products
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('orders_products') as table:
            table.increments('id')

            table.integer('order_id').unsigned()
            table.foreign('order_id').references('id').on('orders')

            table.integer('product_id').unsigned()
            table.foreign('product_id').references('id').on('products')

            table.integer('product_count')
            table.float('unit_price')

            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('orders_products')
