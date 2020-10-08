from orator.migrations import Migration


class ProductsAddNote(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('products') as table:
            table.long_text('note').nullable()

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('products') as table:
            table.drop_column('note')
