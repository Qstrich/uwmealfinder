"""
UW Food Services Steak Finder
Scrapes the University of Waterloo daily menu to find days and locations serving steak.
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import argparse
import sys

# Ensure Unicode characters display correctly on Windows consoles
sys.stdout.reconfigure(encoding="utf-8")

BASE_URL = "https://uwaterloo.ca/food-services-information/locations-and-hours/daily-menu"


def get_menu_for_date(date_str):
    """
    Fetch and parse the menu for a given date.

    Args:
        date_str: Date in YYYY-MM-DD format.

    Returns:
        List of dicts with keys: location, station, item
    """
    params = {"field_uw_fs_dm_date_value[value][date]": date_str}
    response = requests.get(BASE_URL, params=params, timeout=15)
    response.raise_for_status()
    response.encoding = "utf-8"

    soup = BeautifulSoup(response.text, "html.parser")
    menu_items = []

    # Each location is an <li class="dm-location"> followed by <ul class="dm-whole-outlet">
    # They live inside paragraphs-item containers
    location_containers = soup.find_all(
        "div", class_="entity-paragraphs-item"
    )

    current_location = None

    for container in location_containers:
        # Check if this container has a location name
        loc_el = container.find("li", class_="dm-location")
        if loc_el:
            current_location = loc_el.get_text(strip=True)

        # If no location found yet, skip
        if not current_location:
            continue

        # Find station/meal types within this container
        station_el = container.find("li", class_="dm-menu-type")
        if not station_el:
            continue
        station = station_el.get_text(strip=True)

        # Find all menu items
        items_list = container.find("ul", class_="dm-menus")
        if not items_list:
            continue

        for item_el in items_list.find_all("li", class_="dm-menu-item"):
            link = item_el.find("a")
            if link:
                item_name = link.get_text(strip=True)
            else:
                item_name = item_el.get_text(strip=True)

            menu_items.append({
                "location": current_location,
                "station": station,
                "item": item_name,
            })

    # Deduplicate (same location + station + item can appear due to nested containers)
    seen = set()
    unique = []
    for item in menu_items:
        key = (item["location"], item["station"], item["item"])
        if key not in seen:
            seen.add(key)
            unique.append(item)

    return unique


def search_menus(keyword, days, start_date=None):
    """
    Search menus over a range of days for a keyword.

    Args:
        keyword: Search term (case-insensitive).
        days: Number of days to search from start_date.
        start_date: Starting date (defaults to today).

    Returns:
        List of dicts with keys: date, location, station, item
    """
    if start_date is None:
        start_date = datetime.today().date()

    results = []

    for i in range(days):
        date = start_date + timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        day_label = date.strftime("%A, %B %d, %Y")

        print(f"  Checking {day_label}...", end="", flush=True)

        try:
            menu_items = get_menu_for_date(date_str)
        except requests.RequestException as e:
            print(f" [error: {e}]")
            continue

        matches = [
            item for item in menu_items
            if keyword.lower() in item["item"].lower()
        ]

        if matches:
            print(f" found {len(matches)} match(es)!")
            for m in matches:
                results.append({"date": day_label, "date_raw": date_str, **m})
        else:
            print(f" no matches ({len(menu_items)} items scanned)")

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Find when and where steak is served at UW Food Services."
    )
    parser.add_argument(
        "-k", "--keyword",
        default="steak",
        help='Menu item keyword to search for (default: "steak")',
    )
    parser.add_argument(
        "-d", "--days",
        type=int,
        default=14,
        help="Number of days to search ahead (default: 14)",
    )
    parser.add_argument(
        "-s", "--start",
        default=None,
        help="Start date in YYYY-MM-DD format (default: today)",
    )
    args = parser.parse_args()

    if args.start:
        try:
            start_date = datetime.strptime(args.start, "%Y-%m-%d").date()
        except ValueError:
            print(f"Error: Invalid date format '{args.start}'. Use YYYY-MM-DD.")
            sys.exit(1)
    else:
        start_date = datetime.today().date()

    keyword = args.keyword
    print(f'Searching UW Food Services menus for "{keyword}"...')
    print(f"  Date range: {start_date} to {start_date + timedelta(days=args.days - 1)}")
    print(f"  ({args.days} days)\n")

    results = search_menus(keyword, args.days, start_date)

    print()
    if results:
        print("=" * 65)
        print(f'  RESULTS: Found "{keyword}" on {len(results)} menu(s)!')
        print("=" * 65)

        current_date = None
        for r in results:
            if r["date"] != current_date:
                current_date = r["date"]
                print(f"\n  {current_date}")
                print(f"  {'-' * 40}")
            print(f"    Location : {r['location']}")
            print(f"    Station  : {r['station']}")
            print(f"    Item     : {r['item']}")
            print()
    else:
        print("=" * 65)
        print(f'  No "{keyword}" found in the next {args.days} days.')
        print("=" * 65)
        print(f"\n  Tip: Try a broader search, e.g.:")
        print(f'    python find_steak.py --keyword "beef"')
        print(f'    python find_steak.py --keyword "burger"')
        print(f'    python find_steak.py --days 30')


if __name__ == "__main__":
    main()
