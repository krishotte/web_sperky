from orator.migrations import Migration


class OrdersAddNameNote(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('orders') as table:
            table.string('name').nullable()
            table.long_text('note').nullable()

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('orders') as table:
            table.drop_column('name')
            table.drop_column('note')
