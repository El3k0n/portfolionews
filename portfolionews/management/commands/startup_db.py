from django.core.management.base import BaseCommand
from portfolionews.tasks import populate_first_time

class Command(BaseCommand):
    help = "Populate the database without time constraints"

    def handle(self, *args, **options):
        self.stdout.write("Fetching news for the first time...")
        populate_first_time()
