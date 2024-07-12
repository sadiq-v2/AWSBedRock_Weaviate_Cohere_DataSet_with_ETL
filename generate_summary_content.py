# generate_summary_content.py

import pandas as pd
from generate_summaries import generate_education_summary, generate_employment_summary, generate_aggregate_summary

def generate_summary_content(record):
    name = record["name"]
    city = record["city"]
    region = record["region"]
    employments = record.get("employments", [])
    educations = record.get("education", [])

    employment_summary = generate_employment_summary(employments, name, region) if employments else None
    education_summary = generate_education_summary(educations, name) if educations else None
    aggregate_summary = generate_aggregate_summary(employments, name, city) if employments else None

    return {
        "employment_summary": employment_summary,
        "education_summary": education_summary,
        "aggregate_summary": aggregate_summary
    }
