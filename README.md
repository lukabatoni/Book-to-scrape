# BookScraper

BookScraper is a Python project that scrapes book data from [Books to Scrape](http://books.toscrape.com/) using multiprocessing for efficiency. It collects book details from multiple categories and saves the results as JSON files.

## Features

- Scrapes book information (title, price, stock, description) from categories
- Uses multiprocessing to speed up scraping
- Saves results as JSON files in the `output/` directory
- Configurable via `config.json`

## Requirements

- Python 3.7+
- See `requirements.txt` for dependencies:
  - `beautifulsoup4`
  - `requests`
  - `lxml`

Install dependencies with:
```sh
pip install -r requirements.txt
```

## Configuration

Edit `config.json` to set:
- `base_url`: The website to scrape (default: http://books.toscrape.com/)
- `num_workers`: Number of parallel worker processes
- `output_dir`: Directory for output files
- `delay_between_requests`: Delay (in seconds) between requests
- `max_retries`: Number of retries for failed requests

## Usage

Run the scraper with:
```sh
python main.py
```

The script will:
- Start worker processes
- Scrape the first 5 categories (for demo)
- Save each category's books to `output/category_<category>.json`

## Project Structure

```
BookScraper/
├── main.py           # Entry point, master process
├── worker.py         # Worker process logic
├── utils.py          # Utility functions (requests, saving, config)
├── config.json       # Configuration file
├── requirements.txt  # Python dependencies
├── output/           # Scraped data (JSON files)
└── .gitignore        # Files and folders to ignore in git
```

## Notes

- Only JSON files in the `output/` directory are ignored by git.
- You can adjust the number of categories or scraping logic in `main.py`.

## License

For educational/demo use only. Not affiliated with books.toscrape.com.