from django.core.management.base import BaseCommand
from portfolionews.models import Article, Ticker

class Command(BaseCommand):
    help = "Clear all articles and tickers from the database"

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm that you want to delete all data',
        )

    def handle(self, *args, **options):
        if not options['confirm']:
            self.stdout.write(
                self.style.WARNING(
                    "This command will delete ALL articles and tickers from the database!\n"
                    "Use --confirm to proceed."
                )
            )
            return

        # Get counts before deletion
        article_count = Article.objects.count()
        ticker_count = Ticker.objects.count()

        if article_count == 0 and ticker_count == 0:
            self.stdout.write(
                self.style.SUCCESS("Database is already empty. Nothing to delete.")
            )
            return

        # Delete all articles first (due to foreign key relationship)
        self.stdout.write(f"Deleting {article_count} articles...")
        Article.objects.all().delete()

        # Delete all tickers
        self.stdout.write(f"Deleting {ticker_count} tickers...")
        Ticker.objects.all().delete()

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully deleted {article_count} articles and {ticker_count} tickers."
            )
        )
