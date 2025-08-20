from django.core.management.base import BaseCommand
from portfolionews.tasks import update_news

class Command(BaseCommand):
    help = "Manually update the news"

    def handle(self, *args, **options):
        self.stdout.write("Updating news manually...")
        update_news()
