from orator.migrations import Migration


class CreateAvailabilitiesTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('availabilities') as table:
            table.increments('id')
            table.string('name')
            table.string('visual_class').nullable()

            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('availabilities')
