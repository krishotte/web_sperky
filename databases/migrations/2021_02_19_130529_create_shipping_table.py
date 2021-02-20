from orator.migrations import Migration


class CreateShippingTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('shippings') as table:
            table.increments('id')
            table.string('name')
            table.float('price')

            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('shippings')
