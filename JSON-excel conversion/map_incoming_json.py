
import json
from datetime import datetime, timedelta
import pandas as pd

# Category to supercategory mapping
category_supercategory_mapping = {
    'shoes': 'Apparel and accessories',
    'clothes': 'Apparel and accessories',
    'food': 'Food & Beverage',
    'beverage': 'Food & Beverage',
    'isp': 'Services',
    'retail': 'Services',
    'motorbike': 'Transportation and tools',
    'vehicle': 'Transportation and tools',
    # Add more mappings as needed
}

# Urgency calculation function
def calculate_urgency(creation_date, urgency):
    creation_date = datetime.strptime(creation_date, "%Y-%m-%d")
    current_date = datetime.now()

    urgency_threshold = {
        "today": 0,
        "this week": 7,
        "this month": 30
    }

    threshold = urgency_threshold.get(urgency, 30)  # Default to "this month"
    days_until_urgency = (creation_date + timedelta(days=threshold)) - current_date
    if days_until_urgency.days <= 0:
        return 'High'
    elif days_until_urgency.days <= 7:
        return 'Medium'
    else:
        return 'Low'

# Accumulation rate mapping
accumulation_rate_mapping = {
    'Shoes': 'Medium',
    'Food': 'High',
    'Services': 'High',
    'Beverage': 'High',
    'Clothes': 'Medium',
    'Retail': 'High',
    'Vehicle': 'Low'
}

# Priority assignment function based on user preferences
def get_priority(program, user_pref):
    if program in user_pref:
        return f'P{user_pref.index(program) + 1}'
    return None

# Read the json files
with open('userpref2.json', 'r') as f:
    user_preference = json.load(f)

with open('supplies2.json', 'r') as f:
    supplies_data = json.load(f)

# Initialize the final list to store processed data
final_data_with_id = []

# Process each supply item, now including the ID
for supply in supplies_data['supplies']:
    supercategory = category_supercategory_mapping.get(supply['category'].lower(), 'Unknown')
    urgency_of_deal = calculate_urgency(supply['creation_date'], supply['urgency'])
    accumulation_rate = accumulation_rate_mapping.get(supply['category'], 'Unknown')
    prefered_programs = get_priority(supply['program'], user_preference.get(supply['category'], []))

    final_data_with_id.append({
        'ID': supply['id'],
        'Supercategory': supercategory,
        'Prefered Programs': prefered_programs,
        'Accumulation Rate': accumulation_rate,
        'Urgency of Deal': urgency_of_deal
    })

# Convert the final data list with ID to a DataFrame
df_with_id = pd.DataFrame(final_data_with_id)

# Display the DataFrame
print(df_with_id)

# Checking on excel
#df_with_id.to_excel('check.xlsx')
