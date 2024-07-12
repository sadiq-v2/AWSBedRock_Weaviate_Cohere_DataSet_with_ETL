# calculate_experience.py

from datetime import datetime
from parse_dates import parse_date
import pandas as pd

# Function to calculate aggregate experience and average revenue
def create_aggregate_experience(employments):
    if not isinstance(employments, list):
        return 0.0, 0.0

    total_years = 0.0
    total_revenue = 0.0
    count = 0

    for emp in employments:
        start_date = pd.to_datetime(emp.get("started_on"), errors='coerce')
        end_date = pd.to_datetime(emp.get("ended_on"), errors='coerce')
        amount_usd = emp.get("amount_usd", 0.0)

        if pd.isna(start_date) or pd.isna(end_date):
            continue

        years_experience = (end_date - start_date).days / 365.25
        total_years += max(0, years_experience)

        if amount_usd > 0:
            total_revenue += amount_usd
            count += 1

    average_revenue = total_revenue / count if count > 0 else 0.0

    return total_years, average_revenue
