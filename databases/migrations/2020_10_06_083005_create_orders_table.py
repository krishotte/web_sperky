from orator.migrations import Migration


class CreateOrdersTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('orders') as table:
            table.increments('id')
            # user can have many orders
            table.integer('user_id').unsigned()
            table.foreign('user_id').references('id').on('users')

            table.float('shipping_price')
            table.float('total_price')

            # TODO_: order status - separate table order_statuses
            # ordered
            # confirmed
            # ready for shipping
            # shipped
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('orders')
