"""CreateFiles Migration."""

from masoniteorm.migrations import Migration


class CreateFiles(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("files") as table:
            table.uuid("id").primary()
            table.string("name")
            table.string("size")
            table.string("type")
            table.string("user_email")
            table.index("user_email")
            table.soft_deletes()
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("files")
