"""Base Database Seeder Module."""
from masoniteorm.seeds import Seeder


class DatabaseSeeder(Seeder):
    def run(self):
        """Run the database seeds."""
        # self.call(UserTableSeeder)
