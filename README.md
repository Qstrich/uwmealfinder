# UWaterloo Steak Finder 🥩

A Python script that scrapes the [University of Waterloo Food Services website](https://uwaterloo.ca/food-services-information/locations-and-hours/daily-menu) to find when and where steak (or any menu item) is being served.

## Features

- 🔍 Search for any menu item across multiple days
- 📅 Customizable date ranges
- 🏫 Shows location, station, and full item name
- 🎯 Clean, formatted output with progress indicators

## Installation

1. Clone or download this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Search for "steak" in the next 14 days (default):

```bash
python find_steak.py
```

### Custom Keyword

Search for any menu item:

```bash
python find_steak.py --keyword "burger"
python find_steak.py --keyword "chicken"
python find_steak.py --keyword "pasta"
```

### Extended Search Period

Look further ahead:

```bash
python find_steak.py --days 30
```

### Custom Start Date

Search from a specific date:

```bash
python find_steak.py --start 2026-03-01 --days 14
```

### All Options Combined

```bash
python find_steak.py --keyword "beef" --start 2026-02-20 --days 21
```

## Command Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--keyword` | `-k` | Menu item keyword to search for | `"steak"` |
| `--days` | `-d` | Number of days to search ahead | `14` |
| `--start` | `-s` | Start date in YYYY-MM-DD format | Today |

## Example Output

```
Searching UW Food Services menus for "steak"...
  Date range: 2026-02-13 to 2026-02-26
  (14 days)

  Checking Friday, February 13, 2026... found 1 match(es)!
  Checking Saturday, February 14, 2026... no matches (0 items scanned)
  Checking Sunday, February 15, 2026... no matches (0 items scanned)
  Checking Monday, February 16, 2026... no matches (22 items scanned)
  Checking Tuesday, February 17, 2026... found 1 match(es)!
  ...

=================================================================
  RESULTS: Found "steak" on 3 menu(s)!
=================================================================

  Friday, February 13, 2026
  ----------------------------------------
    Location : REVelation - Ron Eydt Village
    Station  : Hot Dish
    Item     : Chimichurri Flank Steak


  Tuesday, February 17, 2026
  ----------------------------------------
    Location : Mudie's - Village 1
    Station  : The Carvery Dinner
    Item     : 8 oz New York Steak with Mushroom Sauce


  Tuesday, February 24, 2026
  ----------------------------------------
    Location : The Market
    Station  : The Carvery Dinner
    Item     : Steak Night
```

## How It Works

1. The script builds URLs for the UW Food Services daily menu page with specific dates
2. It fetches and parses the HTML using BeautifulSoup
3. Extracts menu items organized by location and station
4. Searches for your keyword (case-insensitive) across all items
5. Displays matching results in a formatted output

## Dining Locations

The script searches across all UW Food Services locations including:

- **The Market** (main campus)
- **Mudie's** (Village 1 residence)
- **REVelation** (Ron Eydt Village residence)

## Notes

- Weekend menus may not be available (dining halls often closed)
- Menus are typically posted 1-2 weeks in advance
- The search is case-insensitive
- Special characters in location names (like apostrophes) are properly handled

## Requirements

- Python 3.7+
- requests
- beautifulsoup4

## License

Free to use for finding your steak! 🥩

## Contributing

Found a bug or want to add a feature? Feel free to fork and submit a pull request!

## Disclaimer

This is an unofficial tool and is not affiliated with the University of Waterloo or UW Food Services. Menu information is scraped from publicly available web pages and may not always be up to date.
