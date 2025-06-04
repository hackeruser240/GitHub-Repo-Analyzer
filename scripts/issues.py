import requests

from datetime import datetime, timedelta
from collections import Counter

def get_total_issues(var):

    open_issues = requests.get(f"https://api.github.com/search/issues?q=repo:{var.repo}+is:issue+is:open", headers=var.headers).json()['total_count']


    closed_issues = requests.get(f"https://api.github.com/search/issues?q=repo:{var.repo}+is:issue+is:closed", headers=var.headers
    ).json()['total_count']

    return {"open": open_issues, "closed": closed_issues}

def get_new_issues_by_period(var, days_back=90):
    
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
                all_created_dates.append(created_date)

        page += 1

    weekly_counts = Counter([date.isocalendar()[1] for date in all_created_dates])
    return weekly_counts  # e.g., {22: 45, 23: 38} for week numbers\