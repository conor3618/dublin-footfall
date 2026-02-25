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

def main(output_file="data/footfall_yesterday.json", date_range="yesterday"):
    # Create data folder
    os.makedirs("data", exist_ok=True)
    
    now = datetime.now()
    data_date = (now - timedelta(days=1)).strftime("%Y-%m-%d")
    
    totals = fetch_totals(date_range)
    site_totals = defaultdict(lambda: defaultdict(int))
    
    for record in totals:
        site_id = record["siteId"]
        mode = record["travelMode"]
        value = record.get("value", 0) or 0
        site_totals[site_id][mode] += value
    
    metadata = fetch_metadata()
    
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
    
    final_output = {
        "request_time": now.strftime("%Y-%m-%d %H:%M:%S"),
        "data_date": data_date,
        "sites": sites
    }
    
    with open(output_file, "w") as f:
        json.dump(final_output, f, indent=2)
    
    print(f"Saved data/footfall_yesterday.json")

if __name__ == "__main__":
    main()
