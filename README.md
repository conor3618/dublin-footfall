# Dublin Footfall and Cycle Data

A Python project that queries the [Eco-Counter API](https://data.smartdublin.ie/dataset/pedestrian-and-cycle-counter-api-for-dublin-region) to retrieve pedestrian and bike footfall totals acros the Dublin region. Includes scheduled GitHub Actions that automatically update both historical and current period data daily.

## Features
- Fetches data for yesterday, last week/month/year (historical)
- Captures current week/month/year YTD (current periods)
- Processes 7 distinct time ranges into consistently formatted JSON
- Single metadata fetch optimizes multiple API calls
- GitHub Action runs automatically at 6AM UTC daily
- All JSON files publicly accessible via raw GitHub URLs

## Scripts

| Script | Description | Output Files |
|--------|-------------|--------------|
| `footfall_historical.py` | Historical periods: yesterday, last 7/30/365 days | `footfall_yesterday.json`<br>`footfall_lastweek.json`<br>`footfall_lastmonth.json`<br>`footfall_lastyear.json` |
| `footfall_current.py` | Current periods: week/month/year YTD | `footfall_currentweek.json`<br>`footfall_currentmonth.json`<br>`footfall_currentyear.json` |

## Usage

### Run historical data

    python footfall_historical.py

### Run current period data

    python footfall_current.py

### Run both (full update)

    python footfall_historical.py && python footfall_current.py

## Example Output

```
Saved data/footfall_yesterday.json
Saved data/footfall_lastweek.json
Saved data/footfall_lastmonth.json
Saved data/footfall_lastyear.json
Saved data/footfall_currentweek.json
Saved data/footfall_currentmonth.json
Saved data/footfall_currentyear.json
```

Each JSON contains:
```json
{
  "request_time": "2026-02-26 06:00:00",
  "data_date": "last week (7 days)",
  "sites": [
    {
      "siteId": "12345",
      "name": "O'Connell Street",
      "pedestrian count": 12567,
      "bike count": 234
    }
  ]
}
```
## GitHub Action
Scheduled workflow runs both scripts daily at **6AM UTC** and commits all 7 updated JSON files automatically.

Latest data always available via raw GitHub URLs

## Time Periods

| Period | API Parameter | Label |
|--------|---------------|-------|
| Yesterday | `yesterday` | `YYYY-MM-DD` |
| Last Week | `lastWeek` | `last week (7 days)` |
| Last Month | `lastMonth` | `last month (~30 days)` |
| Last Year | `lastYear` | `last year (365 days)` |
| Current Week | `currentWeek` | `current week (YTD)` |
| Current Month | `currentMonth` | `current month (YTD)` |
| Current Year | `currentYear` | `current year YYYY (YTD)` |

## API Details
```
GET https://api.eco-counter.com/api/v2/statistical/total
?dateRange={yesterday|lastWeek|lastMonth|lastYear|currentWeek|currentMonth|currentYear}
&groupBy=siteAndTravelMode
&validatedDataOnly=false
```

**API Key**: `ebxNfq0IJ3iVH9p6VFEO`

## Data Source
[Smart Dublin - Pedestrian and Cycle Counter API](https://data.smartdublin.ie/dataset/pedestrian-and-cycle-counter-api-for-dublin-region) [developers.eco-counter](https://developers.eco-counter.com)

## Licence
Code is licensed under the MIT License.
