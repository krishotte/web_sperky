from orator.migrations import Migration


class CreateProductsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('products') as table:
            table.increments('id')
            table.string('name')

            # _TODO: product_categories - foreign key
            table.integer('category_id').unsigned()
            table.foreign('category_id').references('id').on('product_categories')

            table.long_text('description')
            table.string('image_folder')
            table.float('price')
            # TODO: attach multiple keywords to the product
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('products')
