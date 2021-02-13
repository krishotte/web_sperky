from orator.migrations import Migration


class AddressesAddSoftdeletes(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('addresses') as table:
            table.soft_deletes()

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('addresses') as table:
            table.drop_soft_deletes()
