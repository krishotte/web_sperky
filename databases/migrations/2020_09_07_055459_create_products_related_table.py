from orator.migrations import Migration


class CreateProductsRelatedTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('products_related') as table:
            table.increments('id')

            table.integer('product_id').unsigned()
            table.foreign('product_id').references('id').on('products')

            table.integer('related_id').unsigned()
            table.foreign('related_id').references('id').on('products')

            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('products_related')
