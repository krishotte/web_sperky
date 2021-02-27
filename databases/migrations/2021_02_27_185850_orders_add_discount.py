from orator.migrations import Migration


class OrdersAddDiscount(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('orders') as table:
            table.float('discount').default(0)

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('orders') as table:
            table.drop_column('discount')
