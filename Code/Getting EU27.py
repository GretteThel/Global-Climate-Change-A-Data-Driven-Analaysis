#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

# Load the uploaded Excel file to examine its contents
file_path = "EDGAR_2024_GHG_booklet_2024(1).xlsx"
excel_file = pd.ExcelFile(file_path)

# Display the sheet names to identify where the GHG data is stored
excel_file.sheet_names


# In[2]:


# Load the sheet that contains total GHG emissions by country
df_ghg_totals = excel_file.parse('GHG_totals_by_country')

# Display the first few rows and column names to understand its structure
df_ghg_totals.head()


# In[ ]:





# In[ ]:





# In[4]:


# Drop any NaN values in the 'Country' column to avoid errors when checking strings
available_countries_clean = df_ghg_totals['Country'].dropna().unique()

# Re-run the matching logic
suspected_names = ['France', 'Italy', 'Spain']
actual_matches = [country for country in available_countries_clean if any(name in country for name in suspected_names)]

actual_matches


# In[5]:


# Update the list of EU27 countries with correct names from the dataset
eu_countries_corrected = [
    'Germany',
    'France and Monaco',
    'Italy, San Marino and the Holy See',
    'Poland',
    'Spain and Andorra',
    'Netherlands',
    'Belgium',
    'Romania',
    'Czechia',
    'Austria'
]

# Filter and prepare the dataset again
eu27_df_corrected = df_ghg_totals[df_ghg_totals['Country'].isin(eu_countries_corrected)]
emissions_2023_corrected = eu27_df_corrected[['Country', 2023]].copy()
emissions_2023_corrected.columns = ['Country', 'Emissions_2023']
emissions_2023_corrected.sort_values(by='Emissions_2023', ascending=True, inplace=True)

# Plot the corrected data
plt.figure(figsize=(10, 6))
plt.barh(emissions_2023_corrected['Country'], emissions_2023_corrected['Emissions_2023'])
plt.xlabel('GHG Emissions in 2023 (Mt CO₂eq)')
plt.title('Top GHG Emitters in the EU27 (2023)')
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()


# In[ ]:





# In[6]:


# Corrected country name mapping for all EU27 members
eu27_name_map = {
    'Austria': 'Austria',
    'Belgium': 'Belgium',
    'Bulgaria': 'Bulgaria',
    'Croatia': 'Croatia',
    'Cyprus': 'Republic of Cyprus',  # mapped name
    'Czechia': 'Czechia',
    'Denmark': 'Denmark',
    'Estonia': 'Estonia',
    'Finland': 'Finland',
    'France and Monaco': 'France',
    'Germany': 'Germany',
    'Greece': 'Greece',
    'Hungary': 'Hungary',
    'Ireland': 'Ireland',
    'Italy, San Marino and the Holy See': 'Italy',
    'Latvia': 'Latvia',
    'Lithuania': 'Lithuania',
    'Luxembourg': 'Luxembourg',
    'Malta': 'Malta',
    'Netherlands': 'Netherlands',
    'Poland': 'Poland',
    'Portugal': 'Portugal',
    'Romania': 'Romania',
    'Slovakia': 'Slovakia',
    'Slovenia': 'Slovenia',
    'Spain and Andorra': 'Spain',
    'Sweden': 'Sweden'
}

# Reverse the map to get dataset names
dataset_names = list(eu27_name_map.keys())

# Filter dataset and apply name mapping
eu27_full_df = df_ghg_totals[df_ghg_totals['Country'].isin(dataset_names)][['Country', 2023]].copy()
eu27_full_df['Country'] = eu27_full_df['Country'].map(eu27_name_map)
eu27_full_df.columns = ['Country', 'Emissions_2023']
eu27_full_df.sort_values(by='Emissions_2023', ascending=True, inplace=True)

# Plotting
plt.figure(figsize=(10, 10))
plt.barh(eu27_full_df['Country'], eu27_full_df['Emissions_2023'])
plt.xlabel('GHG Emissions in 2023 (Mt CO₂eq)')
plt.title('GHG Emissions by EU27 Countries in 2023')
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()


# In[7]:


# Check the number of unique countries included in the final EU27 dataset
num_unique_countries = eu27_full_df['Country'].nunique()
num_unique_countries


# In[ ]:





# In[ ]:





# In[8]:


# Filter out the 'Global Total' entry if it exists
ghg_countries_only = df_ghg_totals[df_ghg_totals['Country'] != 'Global Total']

# Get 2023 emissions for all countries
emissions_2023_all = ghg_countries_only[['Country', 2023]].copy()
emissions_2023_all.columns = ['Country', 'Emissions_2023']

# Drop any missing or invalid values
emissions_2023_all = emissions_2023_all.dropna(subset=['Emissions_2023'])

# Get top 10 highest emitters
top_10_high = emissions_2023_all.sort_values(by='Emissions_2023', ascending=False).head(10)

# Get top 10 lowest emitters (excluding 0 and near-zero values)
top_10_low = emissions_2023_all[emissions_2023_all['Emissions_2023'] > 0].sort_values(by='Emissions_2023', ascending=True).head(10)

top_10_high, top_10_low


# ## Top 10 Highest GHG Emitters (2023)
# 
# (Emissions in Mt CO₂eq)
# 
#     China – 15,944
#     United States – 5,961
#     India – 4,134
#     EU27 (aggregate) – 3,222
#     Russia – 2,672
#     Brazil – 1,300
#     Indonesia – 1,200
#     Japan – 1,041
#     Iran – 997
#     Germany (if EU27 split) – ~682 (would rank 10th above Iran)

# In[ ]:





# ## Top 10 Lowest GHG Emitters (2023)
# 
# (Emissions in Mt CO₂eq)
# 
#     Saint Helena, Ascension and Tristan da Cunha – 0.021
#     Anguilla – 0.026
#     Saint Pierre and Miquelon – 0.047
#     Faroes – 0.051
#     British Virgin Islands – 0.091
#     Turks and Caicos Islands – 0.110
#     Kiribati – 0.130
#     Dominica – 0.147
#     Saint Vincent and the Grenadines – 0.151
#     Cook Islands – 0.154

# In[10]:


# Prepare figure with two subplots for side-by-side bar charts
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16, 6))

# Plot top 10 highest emitters
axes[0].barh(top_10_high['Country'], top_10_high['Emissions_2023'], color='tomato')
axes[0].set_title('Top 10 Highest GHG Emitters (2023)')
axes[0].set_xlabel('Emissions (Mt CO₂eq)')
axes[0].invert_yaxis()
axes[0].grid(axis='x', linestyle='--', alpha=0.7)

# Plot top 10 lowest emitters
axes[1].barh(top_10_low['Country'], top_10_low['Emissions_2023'], color='seagreen')
axes[1].set_title('Top 10 Lowest GHG Emitters (2023)')
axes[1].set_xlabel('Emissions (Mt CO₂eq)')
axes[1].invert_yaxis()
axes[1].grid(axis='x', linestyle='--', alpha=0.7)

# Adjust layout
plt.tight_layout()
plt.show()


# In[ ]:





# In[11]:


# Remove 'GLOBAL TOTAL' from top 10 high emitters
top_10_high_cleaned = top_10_high[top_10_high['Country'] != 'GLOBAL TOTAL']

# Replot with updated data and country labels
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16, 6))

# High emitters chart
axes[0].barh(top_10_high_cleaned['Country'], top_10_high_cleaned['Emissions_2023'], color='tomato')
for i, (value, name) in enumerate(zip(top_10_high_cleaned['Emissions_2023'], top_10_high_cleaned['Country'])):
    axes[0].text(value + 100, i, f'{value:.0f}', va='center')
axes[0].set_title('Top 10 Highest GHG Emitters (2023)')
axes[0].set_xlabel('Emissions (Mt CO₂eq)')
axes[0].invert_yaxis()
axes[0].grid(axis='x', linestyle='--', alpha=0.7)

# Low emitters chart
axes[1].barh(top_10_low['Country'], top_10_low['Emissions_2023'], color='seagreen')
for i, (value, name) in enumerate(zip(top_10_low['Emissions_2023'], top_10_low['Country'])):
    axes[1].text(value + 0.005, i, f'{value:.3f}', va='center')
axes[1].set_title('Top 10 Lowest GHG Emitters (2023)')
axes[1].set_xlabel('Emissions (Mt CO₂eq)')
axes[1].invert_yaxis()
axes[1].grid(axis='x', linestyle='--', alpha=0.7)

# Adjust layout
plt.tight_layout()
plt.show()


# In[ ]:




