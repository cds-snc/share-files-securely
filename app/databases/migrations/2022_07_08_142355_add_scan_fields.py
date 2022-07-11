"""AddScanFields Migration."""

from masoniteorm.migrations import Migration


class AddScanFields(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table("files") as table:
            table.string("av_timestamp").nullable()
            table.string("av_status").nullable()
            table.string("av_scanner").nullable()
            table.string("av_checksum").nullable()

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table("files") as table:
            table.drop_column("av_timestamp")
            table.drop_column("av_status")
            table.drop_column("av_scanner")
            table.drop_column("av_checksum")

