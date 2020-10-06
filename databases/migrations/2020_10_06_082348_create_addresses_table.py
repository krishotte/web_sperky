from orator.migrations import Migration


class CreateAddressesTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('addresses') as table:
            table.increments('id')
            # user can have more addresses
            table.integer('user_id').unsigned()
            table.foreign('user_id').references('id').on('users')

            table.string('street')
            table.string('zip_code')
            table.string('city')

            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('addresses')
