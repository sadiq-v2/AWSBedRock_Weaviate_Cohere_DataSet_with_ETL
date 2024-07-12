# generate_summaries.py

import pandas as pd
from calculate_experience import create_aggregate_experience
from parse_dates import parse_date

def generate_education_summary(educations, name):
    # Function to generate education summary
    if not isinstance(educations, list):
        return f"{name} has no recorded education history."

    if not educations:
        return f"{name} has no recorded education history."

    education_summaries = []
    for edu in educations:
        institution = edu["institution_name"]
        subject = edu.get("subject")
        degree = edu.get("degree")
        end_date = edu.get("ended_on")
        
        # Check for NaN or unknown values
        if pd.isna(subject) or subject == "NaN":
            continue
        if pd.isna(degree) or degree == "NaN":
            continue
        if pd.isna(end_date) or end_date == "NaN":
            continue
        
        education_summary = f"{name} studied {subject} at {institution} and graduated in {end_date}."
        education_summaries.append(education_summary)

    return " ".join(education_summaries)


def generate_employment_summary(employments, name, region):
    if not employments:
        return f"{name} has no recorded work experience."

    sector_list = []
    summary_list = []

    for emp in employments:
        sectors = emp.get("sectors", [])
        seniority = emp.get("seniority_level")
        title = emp.get("title")
        company_name = emp.get("company_name")
        headcount = emp.get("headcount")
        revenue = emp.get("amount_usd")
        ended_on = emp.get("ended_on")

        # Handle NaN values
        if pd.isna(seniority) or seniority == "NaN":
            continue  # Skip this employment record if seniority is NaN or "NaN"
        if pd.isna(company_name) or company_name == "NaN":
            continue
        if pd.isna(headcount) or headcount == "NaN":
            continue
        if pd.isna(revenue) or revenue == "NaN":
            continue

        # Format revenue if it's a number
        if isinstance(revenue, (int, float)):
            revenue = f"{revenue:,.2f}"

        # Handle sectors
        if sectors and isinstance(sectors, list) and any(pd.notna(sector) and sector != "NaN" for sector in sectors):
            sectors = ', '.join(sector for sector in sectors if pd.notna(sector) and sector != "NaN")
        else:
            continue

        employment_status = "is currently working" if ended_on == "NaN" else "has worked"
        region_part = f"and based in {region} region " if pd.notna(region) and region != "NaN" else ""

        summary = (f"{name} {employment_status} as a {seniority}, {title} at {company_name}, "
                   f"a company in the {sectors} sector {region_part}, with {headcount} employees and "
                   f"a revenue of ${revenue}.")
        
        summary_list.append(summary)
        sector_list.extend(sectors.split(', '))

    #flattened_sectors = list(set(sector_list))
    
    full_summary = "\n".join(summary_list)
    return full_summary


# Function to generate aggregate summary
def generate_aggregate_summary(employments, name, city):
    if not isinstance(employments, list):
        return f"{name} has no recorded employment history."

    if not employments:
        return f"{name} has no recorded employment history."

    job_titles = []
    companies = []
    sector_list = []

    for emp in employments:
        title = emp.get("title")
        company_name = emp.get("company_name")
        sectors = emp.get("sectors")
        
        # Check for NaN or unknown values in title and company_name
        if pd.isna(title) or title == "NaN":
            continue
        if pd.isna(company_name) or company_name == "NaN":
            continue
        
        # Check for NaN or unknown values in sectors
        if sectors is None or (isinstance(sectors, list) and not sectors):
            continue
        if isinstance(sectors, list):
            if any(pd.isna(sector) or sector == "NaN" for sector in sectors):
                continue
        else:
            if pd.isna(sectors) or sectors == "NaN":
                continue

        job_titles.append(title)
        companies.append(company_name)
        sector_list.extend(sectors if isinstance(sectors, list) else [sectors])

    if not job_titles or not companies:
        return f"{name} has no valid recorded employment history."

    # Check for NaN in city
    if pd.isna(city) or city == "NaN":
        city_part = ""
    else:
        city_part = f"is currently located in {city} and "

    # Flatten the list of sectors and remove duplicates
    flattened_sectors = list(set(sector_list))

    total_years, average_revenue = create_aggregate_experience(employments)

    summary = (f"{name} {city_part}has over {total_years:.1f} years of experience "
               f"across the following job titles: {', '.join(job_titles)} at companies: {', '.join(companies)} "
               f"in the sectors: {', '.join(flattened_sectors)} with an average revenue size of ${average_revenue:,.2f}.")

    return summary