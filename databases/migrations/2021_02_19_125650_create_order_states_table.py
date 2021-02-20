from orator.migrations import Migration


class CreateOrderStatesTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('order_states') as table:
            table.increments('id')
            table.string('name')
            table.integer('phase').unique()

            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('order_states')
