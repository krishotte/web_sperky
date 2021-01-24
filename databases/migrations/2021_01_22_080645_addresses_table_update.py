from orator.migrations import Migration


class AddressesTableUpdate(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('addresses') as table:
            table.string('name')
            table.string('phone').nullable()

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('addresses') as table:
            table.drop_column('name')
            table.drop_column('phone')
