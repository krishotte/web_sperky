from orator.migrations import Migration


class ProductsCoverImage(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('products') as table:
            table.rename_column('image_folder', 'cover_image')

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('products') as table:
            pass
