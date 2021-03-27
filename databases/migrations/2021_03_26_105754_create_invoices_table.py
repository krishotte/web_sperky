from orator.migrations import Migration


class CreateInvoicesTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('invoices') as table:
            table.increments('id')

            table.string('prefix')
            table.integer('year')
            table.integer('number')
            table.string('variable_symbol').nullable()
            table.date('issue_date')
            table.date('due_date')
            table.boolean('valid').default(True)

            table.integer('order_id').unsigned()
            table.foreign('order_id').references('id').on('orders')

            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('invoices')
