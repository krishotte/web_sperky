from orator.migrations import Migration


class CreateMaterialsProductsTable(Migration):
    """
    many-to-many relationship between products and materials
    """
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('materials_products') as table:
            table.increments('id')

            table.integer('product_id').unsigned()
            table.foreign('product_id').references('id').on('products')

            table.integer('material_id').unsigned()
            table.foreign('material_id').references('id').on('materials')

            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('materials_products')
