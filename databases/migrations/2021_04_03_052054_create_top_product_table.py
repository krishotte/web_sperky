from orator.migrations import Migration


class CreateTopProductTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('top_products') as table:
            table.increments('id')

            table.integer('product_id').unsigned()
            table.foreign('product_id').references('id').on('products')

            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('top_products')
