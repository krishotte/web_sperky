from orator.migrations import Migration


class CreateProductCategoriesTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('categories') as table:
            table.increments('id')

            # TODO: name should be unique
            table.string('name').unique()

            # TODO: order unique

            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('product_categories')
