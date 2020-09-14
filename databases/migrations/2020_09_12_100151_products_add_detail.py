from orator.migrations import Migration


class ProductsAddDetail(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('products') as table:
            table.long_text('detail').nullable()

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('products') as table:
            table.drop_column('detail')
