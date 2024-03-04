import pandas as pd
from itertools import product

def is_favorable(row):
    # Defining weights for different factors
    urgency_factor = 0.5
    scarcity_factor = 0.4
    alignment_factor = 0.3
    bounded_rationality_factor = 0.2

    score = 0

    # Priority of preferred item and merchant alignment
    if row['Preferred Item'] in [1, 2] and row['Preferred Merchant'] in [1, 2]:
        score += alignment_factor * 1.0

    # Scarcity heuristic: boost for low accumulation rate for shoes, clothes, and services
    if row['Preferred Category'] in ['Shoes and Clothes', 'Services']:
        if row['Accumulation Rate'] == 'Low':
            score += scarcity_factor * 0.8
    else:
        if row['Preferred Category'] != 'Food and Beverages' and row['Accumulation Rate'] == 'Low':
            score += scarcity_factor * 0.2

    # Urgency heuristic: prioritize urgency, especially for equipment
    if row['Preferred Category'] == 'Equipment':
        if row['Urgency of Deal'] == 'High':
            score += urgency_factor * 1.0
        elif row['Urgency of Deal'] == 'Medium':
            score += urgency_factor * 0.5
    else:
        if row['Urgency of Deal'] == 'High':
            score += urgency_factor * 1.0
        elif row['Urgency of Deal'] == 'Medium':
            score += urgency_factor * 0.5
        else:
            score += urgency_factor * 0.2

    # Bounded rationality: consider category and merchant for favorability
    if row['Preferred Category'] == 'Food and Beverages':
        if row['Preferred Merchant'] == 1 or row['Preferred Merchant'] == 2:
            score += bounded_rationality_factor * 0.5
    elif row['Preferred Category'] == 'Equipment':
        if row['Accumulation Rate'] == 'Low' and row['Urgency of Deal'] == 'High':
            score += bounded_rationality_factor * 0.8

    # Classify as "Good Deal" or "Bad Deal"
    if score >= 0.6:
        return 'Good Deal'
    else:
        return 'Bad Deal'

# Define possible values for each attribute
categories = ['Food and Beverages', 'Shoes and Clothes', 'Equipment', 'Services']
merchants = [1, 2, 3]
items = [1, 2, 3]
accumulation_rates = ['High', 'Medium', 'Low']
urgency_of_deals = ['High', 'Medium', 'Low']

# Generate all possible combinations of attribute values
combinations = list(product(categories, merchants, items, accumulation_rates, urgency_of_deals))

# Create a DataFrame with unique rows
synthetic_data = pd.DataFrame(combinations, columns=['Preferred Category', 'Preferred Merchant', 'Preferred Item', 'Accumulation Rate', 'Urgency of Deal'])

# Add a column for Favorable Deal using the is_favorable function
synthetic_data['Favorable Deal'] = synthetic_data.apply(is_favorable, axis=1)

# Display the synthetic dataset
print(synthetic_data)

# Write the DataFrame to an Excel file
synthetic_data.to_excel('data.xlsx', sheet_name='Sheet1', index=False)
