from orator.migrations import Migration


class UsersAddRole(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('users') as table:
            table.integer('role_id').unsigned().nullable()
            table.foreign('role_id').references('id').on('roles')

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('users') as table:
            table.drop_column('role_id')
