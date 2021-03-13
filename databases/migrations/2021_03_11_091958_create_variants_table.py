from orator.migrations import Migration


class CreateVariantsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('variants') as table:
            table.increments('id')

            table.integer('product_id').unsigned()
            table.foreign('product_id').references('id').on('products')

            table.string('name')
            table.float('price').nullable()
            table.string('image')

            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('variants')
