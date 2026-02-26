import requests
import json
import os
from datetime import datetime, timedelta
from collections import defaultdict

BASE_URL = "https://api.eco-counter.com/api/v2"
API_KEY = "ebxNfq0IJ3iVH9p6VFEO"
HEADERS = {"accept": "application/json", "X-API-KEY": API_KEY}

def fetch_totals(date_range="yesterday"):
    params = {"dateRange": date_range, "groupBy": "siteAndTravelMode", "validatedDataOnly": "false"}
    resp = requests.get(f"{BASE_URL}/statistical/total", headers=HEADERS, params=params)
    return resp.json() if resp.status_code == 200 else []

def fetch_metadata():
    params = {"page": 1, "pageSize": 100, "sortBy": "id", "orderBy": "asc"}
    resp = requests.get(f"{BASE_URL}/sites", headers=HEADERS, params=params)
    return {str(site["id"]): site for site in resp.json()} if resp.status_code == 200 else {}

def process_data(totals, metadata, data_date):
    site_totals = defaultdict(lambda: defaultdict(int))
    
    for record in totals:
        site_id = record["siteId"]
        mode = record["travelMode"]
        value = record.get("value", 0) or 0
        site_totals[site_id][mode] += value
    
    sites = []
    for site_id, modes in site_totals.items():
        site = {
            "siteId": site_id,
            "pedestrian count": int(modes["pedestrian"]),
            "bike count": int(modes.get("bike", 0)),
            "name": metadata.get(str(site_id), {}).get("name", f"ID{site_id}")
        }
        sites.append(site)
    
    sites.sort(key=lambda x: x["pedestrian count"], reverse=True)
    
    return {
        "request_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "data_date": data_date,
        "sites": sites
    }

def main():
    # Create data folder
    os.makedirs("data", exist_ok=True)
    
    now = datetime.now()
    
    # Yesterday's data
    yesterday_totals = fetch_totals("yesterday")
    metadata = fetch_metadata()
    yesterday_date = (now - timedelta(days=1)).strftime("%Y-%m-%d")
    yesterday_data = process_data(yesterday_totals, metadata, yesterday_date)
    
    yesterday_file = "data/footfall_yesterday.json"
    with open(yesterday_file, "w") as f:
        json.dump(yesterday_data, f, indent=2)
    print(f"Saved {yesterday_file}")
    
    # Last week's data
    lastweek_totals = fetch_totals("lastWeek")
    lastweek_data_date = "last week (7 days)"
    lastweek_data = process_data(lastweek_totals, metadata, lastweek_data_date)
    
    lastweek_file = "data/footfall_lastweek.json"
    with open(lastweek_file, "w") as f:
        json.dump(lastweek_data, f, indent=2)
    print(f"Saved {lastweek_file}")
    
    # Last month's data
    lastmonth_totals = fetch_totals("lastMonth")
    lastmonth_data_date = "last month (~30 days)"
    lastmonth_data = process_data(lastmonth_totals, metadata, lastmonth_data_date)
    
    lastmonth_file = "data/footfall_lastmonth.json"
    with open(lastmonth_file, "w") as f:
        json.dump(lastmonth_data, f, indent=2)
    print(f"Saved {lastmonth_file}")
    
    # Last year's data
    lastyear_totals = fetch_totals("lastYear")
    lastyear_data_date = "last year (365 days)"
    lastyear_data = process_data(lastyear_totals, metadata, lastyear_data_date)
    
    lastyear_file = "data/footfall_lastyear.json"
    with open(lastyear_file, "w") as f:
        json.dump(lastyear_data, f, indent=2)
    print(f"Saved {lastyear_file}")

if __name__ == "__main__":
    main()
