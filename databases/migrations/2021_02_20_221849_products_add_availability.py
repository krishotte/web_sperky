from orator.migrations import Migration


class ProductsAddAvailability(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('products') as table:
            table.integer('availability_id').unsigned().default(1)
            table.foreign('availability_id').references('id').on('availabilities')

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('products') as table:
            table.drop_column('availability_id')
