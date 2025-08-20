from django.core.management.base import BaseCommand
from portfolionews.models import Ticker

class Command(BaseCommand):
    help = "Add tickers to the database"

    def add_arguments(self, parser):
        parser.add_argument(
            'tickers',
            nargs='+',
            help='List of ticker symbols to add (e.g., AAPL MSFT GOOGL)'
        )
        parser.add_argument(
            '--names',
            nargs='+',
            help='List of company names corresponding to tickers (optional)'
        )

    def handle(self, *args, **options):
        ticker_symbols = options['tickers']
        company_names = options.get('names', [])
        
        # If names are provided, they must match the number of tickers
        if company_names and len(company_names) != len(ticker_symbols):
            self.stdout.write(
                self.style.ERROR(
                    f"Number of names ({len(company_names)}) must match number of tickers ({len(ticker_symbols)})"
                )
            )
            return

        added_count = 0
        skipped_count = 0

        for i, symbol in enumerate(ticker_symbols):
            symbol = symbol.upper().strip()
            
            # Check if ticker already exists
            if Ticker.objects.filter(symbol=symbol).exists():
                self.stdout.write(
                    self.style.WARNING(f"Ticker {symbol} already exists, skipping...")
                )
                skipped_count += 1
                continue

            # Create new ticker
            try:
                if company_names:
                    name = company_names[i].strip()
                else:
                    # Use symbol as name if no name provided
                    name = symbol

                ticker = Ticker.objects.create(
                    name=name,
                    symbol=symbol
                )
                
                self.stdout.write(
                    self.style.SUCCESS(f"Added ticker: {symbol} ({name})")
                )
                added_count += 1

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Error adding ticker {symbol}: {e}")
                )

        # Summary
        if added_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f"\nSuccessfully added {added_count} ticker(s)")
            )
        
        if skipped_count > 0:
            self.stdout.write(
                self.style.WARNING(f"Skipped {skipped_count} existing ticker(s)")
            )

        if added_count == 0 and skipped_count == 0:
            self.stdout.write(
                self.style.ERROR("No tickers were added")
            )
