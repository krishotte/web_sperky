from orator.migrations import Migration


class OrdersProductsAddVariant(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('orders_products') as table:
            table.integer('variant_id').unsigned().nullable()
            table.foreign('variant_id').references('id').on('variants')

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('orders_products') as table:
            table.drop_column('variant_id')
