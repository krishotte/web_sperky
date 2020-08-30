from orator.migrations import Migration


class CreateMaterialsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('materials') as table:
            table.increments('id')
            table.string('name').unique()
            table.string('image_path').nullable()
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('materials')
