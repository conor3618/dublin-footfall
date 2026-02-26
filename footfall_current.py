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
    metadata = fetch_metadata()
    
    current_year = now.strftime("%Y")
    
    # Current week's data
    currentweek_totals = fetch_totals("currentWeek")
    currentweek_data_date = "current week (YTD)"
    currentweek_data = process_data(currentweek_totals, metadata, currentweek_data_date)
    
    currentweek_file = "data/footfall_currentweek.json"
    with open(currentweek_file, "w") as f:
        json.dump(currentweek_data, f, indent=2)
    print(f"Saved {currentweek_file}")
    
    # Current month's data
    currentmonth_totals = fetch_totals("currentMonth")
    currentmonth_data_date = "current month (YTD)"
    currentmonth_data = process_data(currentmonth_totals, metadata, currentmonth_data_date)
    
    currentmonth_file = "data/footfall_currentmonth.json"
    with open(currentmonth_file, "w") as f:
        json.dump(currentmonth_data, f, indent=2)
    print(f"Saved {currentmonth_file}")
    
    # Current year's data
    currentyear_totals = fetch_totals("currentYear")
    currentyear_data_date = f"current year {current_year} (YTD)"
    currentyear_data = process_data(currentyear_totals, metadata, currentyear_data_date)
    
    currentyear_file = "data/footfall_currentyear.json"
    with open(currentyear_file, "w") as f:
        json.dump(currentyear_data, f, indent=2)
    print(f"Saved {currentyear_file}")

if __name__ == "__main__":
    main()
