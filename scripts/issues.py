import requests
import calendar
import matplotlib.pyplot as plt

from scripts.helperFunctions import save_fig
from datetime import date,datetime, timedelta
from collections import Counter
from concurrent.futures import ThreadPoolExecutor



def get_total_issues(var):
    def fetch_issues(state):
        url = f"https://api.github.com/search/issues?q=repo:{var.repo}+is:issue+is:{state}"
        response = requests.get(url, headers=var.headers)
        return response.json()['total_count']

    with ThreadPoolExecutor(max_workers=2) as executor:
        future_open = executor.submit(fetch_issues, "open")
        future_closed = executor.submit(fetch_issues, "closed")

        open_issues = future_open.result()
        closed_issues = future_closed.result()

    return {"open": open_issues, "closed": closed_issues}

def get_new_issues_by_period(var, days_back=50,cutoff_year=2025):
    
    per_page = 100
    page = 1
    since = (datetime.utcnow() - timedelta(days=days_back)).isoformat() + "Z"
    all_created_dates = []

    while True:
        url = f"https://api.github.com/repos/{var.repo}/issues?state=all&since={since}&per_page={per_page}&page={page}"
        response = requests.get(url, headers=var.headers).json()

        if not response:
            break

        for issue in response:
            if 'pull_request' not in issue:  # Exclude PRs
                created_date = datetime.strptime(issue['created_at'], "%Y-%m-%dT%H:%M:%SZ").date()
                if created_date.year >= cutoff_year:
                    all_created_dates.append(created_date)

        page += 1
    
    weekly_counts = Counter([date.isocalendar()[1] for date in all_created_dates])
    return weekly_counts  # e.g., {22: 45, 23: 38} for week numbers

def print_weekly_issue_summary(weekly_counts, year=2025):
    for week_num in sorted(weekly_counts.keys()):
        # Get the start and end date for the ISO week
        start_date = date.fromisocalendar(year, week_num, 1)  # Monday
        end_date = date.fromisocalendar(year, week_num, 7)    # Sunday

        # Format date range
        date_range = f"{start_date.strftime('%b %d')}–{end_date.strftime('%b %d')}"
        
        # Get number of issues
        count = weekly_counts[week_num]

        # Print in desired format
        print(f"Week {week_num} ({date_range}): {count} issue{'s' if count != 1 else ''}")

def plot(weekly_counts):
    weeks = sorted(weekly_counts.keys())
    issues = [weekly_counts[week] for week in weeks]

    plt.figure(figsize=(12, 6))
    plt.plot(weeks, issues, marker='o', linestyle='-', color='royalblue')

    # Labels and title
    plt.xlabel("Week Number")
    plt.ylabel("Number of Issues")
    plt.title("GitHub Issues per Week (2025)")
    plt.grid(True)
    plt.xticks(weeks, rotation=45)

    # Annotate each point (optional)
    for week, count in zip(weeks, issues):
        plt.text(week, count + 0.5, str(count), ha='center', fontsize=8)

    plt.tight_layout()
    #plt.show()
    save_fig("Issues per Week.png")