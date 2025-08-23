# Portfolio News

I built this simple Django app to get a personalized RSS feed relative to the tickers that interest me.
Surprisingly, I couldn't find anything similar for free, only specialized subscription-based services.

After the initial setup, the application will fetch news every hour and render them as a feed at `http://127.0.0.1:8000/rss`

The app also tries to download each entry's text using the newspaper3k library.

## Setup

### 1. Clone and Install Dependencies
```bash
git clone https://github.com/El3k0n/portfolionews.git
cd portfolionews

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt
```

You'll also need to set the environment variables. If you're only testing it, you can make the following changes to ```settings.py```:

```python
SECRET_KEY = "your-very-unsafe-secret-key"
DEBUG = 1
ALLOWED_HOSTS = [*]
```

And delete these lines at the end of the same file:
```python
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = getenv_bool("DJANGO_SECURE_SSL_REDIRECT","1")
CSRF_TRUSTED_ORIGINS = [f"https://{h}" for h in ALLOWED_HOSTS if h]
```

### 2. Database Setup
```bash
# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

### 3. Add Tickers
You can add the first tickers with the dedicated Django command:

```bash
# Add individual tickers
python manage.py add_ticker AAPL MSFT GOOGL --names "Apple Inc." "Microsoft Corporation" "Alphabet Inc."

# Or add tickers without custom names
python manage.py add_ticker TSLA NVDA
```

Alternatively you can do it graphically in the next step

### 4. Start Development Server
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`, simply opening that link will allow you to add tickers graphically

## Crontab Configuration
The system uses crontab to fetch the news periodically:

### 1. Install Crontab Jobs
```bash
# Add cron jobs to system
python manage.py crontab add

# Verify installation
python manage.py crontab show

# Remove cron jobs (if needed)
python manage.py crontab remove
```

### 2. Cron Job Schedule
- **Update News**: Every hour (`0 * * * *`)

### 3. Manual Task Execution
```bash
# Update news manually
python manage.py update_news

# Populate news for first time
python manage.py populate_first_time
```

## Management Commands

- `add_ticker`: Add new tickers to database
- `update_news`: Fetch latest news for existing tickers
- `populate_first_time`: Fetch all available news for tickers
- `clear_data`: Remove all articles and tickers (use with `--confirm`)


## Dependencies

- Django 5.1.3+
- django-crontab 0.7.1+
- yfinance 0.2.29+
- newspaper3k 0.2.8+
- requests 2.31.0+
- sqids 0.5.2+
- python-dateutil 2.8.2+

## Notes

- Ensure your virtual environment is activated before running any commands
- The application uses SQLite by default for development
- Crontab jobs require the system cron daemon to be running
- News fetching is limited to tickers present in the database
