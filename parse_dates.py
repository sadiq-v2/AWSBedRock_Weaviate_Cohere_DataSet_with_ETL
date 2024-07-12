# parse_dates.py

import pandas as pd
from datetime import datetime

def parse_date(date_str):
    if pd.isna(date_str) or date_str == 'NaN':
        return None  # Handle missing or NaN values
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        try:
            return datetime.strptime(date_str, '%m/%d/%Y')
        except ValueError:
            return None  # Handle unrecognized date formats as needed
