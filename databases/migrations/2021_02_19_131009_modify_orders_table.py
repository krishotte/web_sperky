from orator.migrations import Migration


class ModifyOrdersTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('orders') as table:
            table.integer('order_state_id').unsigned()
            table.foreign('order_state_id').references('id').on('order_states')

            table.integer('shipping_id').unsigned()
            table.foreign('shipping_id').references('id').on('shippings')

            table.integer('address_id').unsigned()
            table.foreign('address_id').references('id').on('addresses')

            table.drop_column('shipping_price')

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('orders') as table:
            table.drop_column('order_state_id')
            table.drop_column('shipping_id')
            table.drop_column('address_id')

            table.float('shipping_price').nullable()
