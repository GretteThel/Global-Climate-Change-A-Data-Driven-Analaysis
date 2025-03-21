#!/usr/bin/env python
# coding: utf-8

# In[62]:


pip install matplotlib pandas numpy


# In[63]:


import pandas as pd

# Load the Excel file
file_path_ghg = "EDGAR_2024_GHG_booklet_2024(1).xlsx"


# Check the sheet names to understand the structure of the data
xls_ghg = pd.ExcelFile(file_path_ghg)


xls_ghg.sheet_names


# # GLOBAL SECTOR

# In[64]:


# Load the GHG emissions by sector and country sheet
df_ghg_sector = pd.read_excel(xls_ghg, sheet_name="GHG_by_sector_and_country")

# Display the first few rows to understand the structure
df_ghg_sector.head()


# 
# The **GHG_by_sector_and_country** dataset contains:
# - **Substance**: Type of greenhouse gas (CO₂, CH₄, etc.)
# - **Sector**: The economic sector responsible for emissions (Agriculture, Transport, Power Industry, etc.)
# - **Country**: Country name and code
# - **Yearly emissions**: Columns representing emissions per year from 1970 to 2023
# 
# To create the graphs similar to those in the images, we need to:
# 1. Filter data for **total world emissions** across sectors.
# 2. Sum emissions by sector for each year.
# 3. Create stacked bar charts for different years and sectors.
# 4. Include pie charts for gas composition (CO₂, CH₄, etc.).
# 5. Compute percentage increases for sectoral comparisons.

# In[65]:


# Summarize global emissions by sector for each year
df_global_sector = df_ghg_sector.drop(columns=["Country", "Substance"], errors='ignore').groupby("Sector").sum(numeric_only=True)

# Transpose the dataframe for better visualization
df_global_sector_transposed = df_global_sector.T

# Display first few rows of the transposed dataframe for verification
df_global_sector_transposed.head()


# In[ ]:





# In[ ]:





# # BY SECTOR and COUNTRY

# In[66]:


import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel file
file_path_ghg = "EDGAR_2024_GHG_booklet_2024(1).xlsx"

# Check the sheet names to understand the structure of the data
xls_ghg = pd.ExcelFile(file_path_ghg)

# Step 1: Reload the "GHG_by_sector_and_country" sheet to ensure correct global emissions
global_ghg_data = xls_ghg.parse("GHG_by_sector_and_country")

# Step 2: Filter data where "Country" and "EDGAR Country Code" are labeled as "GLOBAL TOTAL"
global_ghg_data = global_ghg_data[
    (global_ghg_data["Country"] == "GLOBAL TOTAL") &
    (global_ghg_data["EDGAR Country Code"] == "GLOBAL TOTAL")
]

# Step 3: Select only relevant columns: Yearly Emissions (1990-2023)
years_range = list(range(1990, 2024))

global_total_emissions = global_ghg_data[years_range].sum()

# Step 4: Convert the summed emissions into a DataFrame for plotting
global_total_emissions_df = pd.DataFrame(global_total_emissions, columns=["Global GHG Emissions (Mt CO2eq/yr)"])

# Step 5: Convert index to integer for proper plotting
global_total_emissions_df.index = global_total_emissions_df.index.astype(int)

# Step 6: Generate a corrected line chart for global emissions (1990-2023)
plt.figure(figsize=(12, 6))
plt.plot(
    global_total_emissions_df.index, 
    global_total_emissions_df["Global GHG Emissions (Mt CO2eq/yr)"], 
    marker="o", linestyle="-", color="blue"
)

# Customize the plot
plt.xlabel("Year")
plt.ylabel("GHG Emissions (Mt CO2eq)")
plt.title("Global GHG Emissions (1990-2023)")
plt.xticks(rotation=45)
plt.grid(True)

# Show the chart
plt.show()


# In[ ]:





# In[67]:


import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel file
file_path_ghg = "EDGAR_2024_GHG_booklet_2024(1).xlsx"
xls_ghg = pd.ExcelFile(file_path_ghg)

# Step 1: Reload the "GHG_by_sector_and_country" sheet
global_ghg_data = xls_ghg.parse("GHG_by_sector_and_country")

# Step 2: Filter data where "Country" and "EDGAR Country Code" are labeled as "GLOBAL TOTAL"
global_ghg_data = global_ghg_data[
    (global_ghg_data["Country"] == "GLOBAL TOTAL") & 
    (global_ghg_data["EDGAR Country Code"] == "GLOBAL TOTAL")
]

# Step 3: Select only relevant columns: Sector and Yearly Emissions (1990-2023)
years_range = list(range(1990, 2024))

global_ghg_data = global_ghg_data[["Sector"] + years_range]

# Step 4: Sum emissions for each sector over time
sector_emissions_over_time = global_ghg_data.groupby("Sector").sum(numeric_only=True)

# Step 5: Generate a stacked bar chart for global emissions (1990-2023)
plt.figure(figsize=(14, 7))
sector_emissions_over_time.T.plot(kind="bar", stacked=True, figsize=(14, 7), width=0.8, legend=True)

# Customize the plot
plt.xlabel("Year")
plt.ylabel("GHG Emissions (Mt CO2eq)")
plt.title("Global GHG Emissions by Sector (1990-2023)")
plt.xticks(rotation=45)
plt.legend(title="Sector", bbox_to_anchor=(1.05, 1), loc="upper left")

# Show the chart
plt.show()


# In[ ]:





# In[68]:


import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel file
file_path_ghg = "EDGAR_2024_GHG_booklet_2024(1).xlsx"
xls_ghg = pd.ExcelFile(file_path_ghg)

# Step 1: Reload the "GHG_by_sector_and_country" sheet
global_ghg_data = xls_ghg.parse("GHG_by_sector_and_country")

# Step 2: Filter data where "Country" and "EDGAR Country Code" are labeled as "GLOBAL TOTAL"
global_total_emissions = global_ghg_data[(global_ghg_data["Country"] == "GLOBAL TOTAL") & 
                                         (global_ghg_data["EDGAR Country Code"] == "GLOBAL TOTAL")]

# Step 3: Select only relevant year columns (1990, 2005, 2015, 2023) and sum across all sectors
selected_years = [1990, 2005, 2015, 2023]
global_total_emissions = global_total_emissions[selected_years].sum().reset_index()

# Step 4: Rename columns for clarity
global_total_emissions.columns = ["Year", "GHG Emissions (Mt CO2eq/yr)"]

# Step 5: Define Population data (as extracted from the reference image)
population_values = {
    1990: 5.330e9,  # Convert from billion to absolute numbers
    2005: 6.540e9,
    2015: 7.381e9,
    2023: 8.032e9
}

# Add population data to DataFrame
global_total_emissions["Population"] = global_total_emissions["Year"].map(population_values)

# Step 6: Compute GHG emissions per capita using the formula:
global_total_emissions["GHG Emissions per Capita (t CO2eq/cap/yr)"] = (
    global_total_emissions["GHG Emissions (Mt CO2eq/yr)"] * 1e6 / global_total_emissions["Population"]
).round(3)

# Step 7: Define GDP data (from reference image)
gdp_values = {
    1990: 60.3e12,  # Convert from trillion to absolute numbers
    2005: 94.5e12,
    2015: 132.2e12,
    2023: 165.6e12
}

# Add GDP data to DataFrame
global_total_emissions["GDP_kUSD"] = global_total_emissions["Year"].map(gdp_values) * 1e3  # Convert from Trillion to Billion USD

# Step 8: Compute GHG emissions per GDP using the formula:
global_total_emissions["GHG Emissions per unit of GDP PPP (t CO2eq/kUSD/yr)"] = (
    global_total_emissions["GHG Emissions (Mt CO2eq/yr)"] * 1e6 / global_total_emissions["GDP_kUSD"]
).round(3)

# Step 9: Convert Population to billions for readability
global_total_emissions["Population"] = (global_total_emissions["Population"] / 1e9).round(3).astype(str) + "G"

# Step 10: Remove the extra GDP column
global_total_emissions = global_total_emissions.drop(columns=["GDP_kUSD"])

# Step 11: Display the final computed table
display(global_total_emissions)

# Step 12: Generate a line chart for global emissions (1990-2023)
plt.figure(figsize=(10, 5))
plt.plot(global_total_emissions["Year"], global_total_emissions["GHG Emissions (Mt CO2eq/yr)"], 
         marker="o", linestyle="-", color="blue")

# Customize the plot
plt.xlabel("Year")
plt.ylabel("GHG Emissions (Mt CO2eq)")
plt.title("Global GHG Emissions (1990-2023)")
plt.xticks(rotation=45)
plt.grid(True)

# Show the chart
plt.show()


# In[69]:


# Step 1: Sort the DataFrame in descending order based on Year
global_total_emissions_sorted = global_total_emissions.sort_values(by="Year", ascending=False)

# Step 2: Display the sorted DataFrame
display(global_total_emissions_sorted)

# Step 3: Generate a line chart with descending year order
plt.figure(figsize=(10, 5))
plt.plot(global_total_emissions_sorted["Year"], global_total_emissions_sorted["GHG Emissions (Mt CO2eq/yr)"], 
         marker="o", linestyle="-", color="blue")

# Customize the plot
plt.xlabel("Year")
plt.ylabel("GHG Emissions (Mt CO2eq)")
plt.title("Global GHG Emissions (1990-2023) - Descending Order")
plt.xticks(rotation=45)
plt.gca().invert_xaxis()  # Invert the x-axis for descending order visualization
plt.grid(True)

# Show the chart
plt.show()


# In[ ]:





# In[70]:


# Step 1: Define GDP values in absolute numbers (Million USD)
gdp_values_million = {
    1990: 60.3e6,  # Convert from Trillion to Million USD (kUSD)
    2005: 94.5e6,
    2015: 132.2e6,
    2023: 165.6e6
}

# Step 2: Map GDP values to the dataset
global_total_emissions_sorted["GDP (Million USD)"] = global_total_emissions_sorted["Year"].map(gdp_values_million)

# Step 3: Compute GHG per GDP using the correct scale
# Ensuring GDP is properly converted into kUSD
global_total_emissions_sorted["GHG Emissions per unit of GDP PPP (t CO2eq/kUSD/yr)"] = (
    global_total_emissions_sorted["GHG Emissions (Mt CO2eq/yr)"] * 1e3 / global_total_emissions_sorted["GDP (Million USD)"]
).round(3)

# Step 4: Drop the extra GDP column
global_total_emissions_sorted = global_total_emissions_sorted.drop(columns=["GDP (Million USD)"])

# Step 5: Display the final corrected table
display(global_total_emissions_sorted)


# In[ ]:





# In[71]:


# Step 1: Define GDP values in absolute numbers (Million USD)
gdp_values_million = {
    1990: 60.3e6,  # Convert from Trillion to Million USD (kUSD)
    2005: 94.5e6,
    2015: 132.2e6,
    2023: 165.6e6
}

# Step 2: Map GDP values to the dataset
global_total_emissions["GDP (Million USD)"] = global_total_emissions["Year"].map(gdp_values_million)

# Step 3: Compute GHG per GDP using the correct scale
global_total_emissions["GHG Emissions per unit of GDP PPP (t CO2eq/kUSD/yr)"] = (
    global_total_emissions["GHG Emissions (Mt CO2eq/yr)"] * 1e3 / global_total_emissions["GDP (Million USD)"]
).round(3)

# Step 4: Drop the extra GDP column
global_total_emissions = global_total_emissions.drop(columns=["GDP (Million USD)"])

# Step 5: Sort the DataFrame in descending order based on Year
global_total_emissions_sorted = global_total_emissions.sort_values(by="Year", ascending=False)

# Step 6: Display the sorted DataFrame
display(global_total_emissions_sorted)

# Step 7: Generate a line chart with descending year order
plt.figure(figsize=(10, 5))
plt.plot(global_total_emissions_sorted["Year"], global_total_emissions_sorted["GHG Emissions (Mt CO2eq/yr)"], 
         marker="o", linestyle="-", color="blue")

# Customize the plot
plt.xlabel("Year")
plt.ylabel("GHG Emissions (Mt CO2eq)")
plt.title("Global GHG Emissions (1990-2023) - Descending Order")
plt.xticks(rotation=45)
plt.gca().invert_xaxis()  # Invert the x-axis for descending order visualization
plt.grid(True)

# Show the chart
plt.show()


# In[ ]:





# In[72]:


# Step 1: Extract emissions for Global Total by sector for relevant years (1990, 2005, 2022, 2023)
comparison_years = [1990, 2005, 2022, 2023]
global_sector_comparison = global_ghg_data[global_ghg_data["Country"] == "GLOBAL TOTAL"]

# Step 2: Select only the relevant year columns
global_sector_comparison = global_sector_comparison[["Sector"] + comparison_years]

# Step 3: Sum emissions for each sector over selected years
sector_emissions_comparison = global_sector_comparison.groupby("Sector").sum(numeric_only=True)

# Step 4: Compute percentage changes for each sector and round off values
percentage_changes = sector_emissions_comparison.copy()

for year_pair in [(2023, 1990), (2023, 2005), (2023, 2022)]:
    year_1, year_2 = year_pair
    column_name = f"{year_1} vs {year_2} (%)"
    percentage_changes[column_name] = (
        (sector_emissions_comparison[year_1] - sector_emissions_comparison[year_2])
        / sector_emissions_comparison[year_2]
    ) * 100
    percentage_changes[column_name] = percentage_changes[column_name].round(0)  # Round to whole numbers

# Step 5: Format the results into a structured table
formatted_table_no_ace = percentage_changes[["2023 vs 1990 (%)", "2023 vs 2005 (%)", "2023 vs 2022 (%)"]].reset_index()

# Function to format percentage change values with arrows
def format_percentage(value):
    if value > 2:
        return f"\033[91m↗ +{int(value)}%\033[0m"  # Red upward arrow for significant increases
    elif 0 < value <= 2:
        return f"\033[93m→ +{int(value)}%\033[0m"  # Orange right arrow for small increases
    elif value == 0:
        return f"\033[93m→ {int(value)}%\033[0m"  # Orange right arrow → (0% change)
    else:
        return f"\033[92m↘ {int(value)}%\033[0m"  # Green downward arrow for decreases

# Apply formatting to the percentage change columns
for col in ["2023 vs 1990 (%)", "2023 vs 2005 (%)", "2023 vs 2022 (%)"]:
    formatted_table_no_ace[col] = formatted_table_no_ace[col].apply(format_percentage)

# Step 6: Sort the table in ascending order by the "2023 vs 1990 (%)" column
formatted_table_no_ace_sorted = formatted_table_no_ace.sort_values(by="2023 vs 1990 (%)", ascending=True)

# Step 7: Display the final formatted table without ace_tools
print("\n\033[1mGlobal GHG Emissions Trends with Colored Arrows (Sorted in Ascending Order)\033[0m")
print(formatted_table_no_ace_sorted.to_string(index=False))


# In[73]:


# Import required libraries
import matplotlib.pyplot as plt

# Step 1: Extract GHG emissions by substance for the year 2023
ghg_2023 = global_ghg_data[global_ghg_data["Country"] == "GLOBAL TOTAL"]

# Step 2: Select relevant columns (Substance and 2023 emissions)
ghg_2023_substances = ghg_2023.groupby("Substance")[2023].sum().reset_index()

# Step 3: Compute total emissions for 2023
total_ghg_2023 = ghg_2023_substances[2023].sum()

# Step 4: Compute percentage share for each substance
ghg_2023_substances["Percentage (%)"] = (ghg_2023_substances[2023] / total_ghg_2023) * 100

# Step 5: Define proper labels for substances
ghg_labels = {
    "CO2": "CO2",
    "GWP_100_AR5_CH4": "CH4",
    "GWP_100_AR5_N2O": "N2O",
    "GWP_100_AR5_F-gases": "F-gases"
}

# Step 6: Replace technical names with proper labels
ghg_2023_substances["Substance"] = ghg_2023_substances["Substance"].replace(ghg_labels)

# Step 7: Update labels for the pie chart
ghg_2023_substances["Label"] = ghg_2023_substances["Substance"] + " " + ghg_2023_substances["Percentage (%)"].round(1).astype(str)



# Step 8: Generate Pie Chart with shades of blue
plt.figure(figsize=(6,6))
plt.pie(
    ghg_2023_substances["Percentage (%)"], 
    labels=ghg_2023_substances["Label"], 
    autopct='', 
    startangle=140, 
    colors=["#1f77b4", "#aec7e8", "#ffbb78", "#c5b0d5"]  # Different shades of blue
)

# Add title
plt.title("GHG % in 2023 By Sector")

# Show the chart
plt.show()


# In[74]:


# Define reference years for percentage change calculations
years_reference = [1990, 2005, 2022, 2023]

# Filter data for the selected years
df_percentage_change = df_global_sector_transposed.loc[years_reference]

# Compute percentage changes
df_percentage_change = df_percentage_change.pct_change() * 100

# Round values for better readability
df_percentage_change = df_percentage_change.round(1)

# Display the computed percentage changes
df_percentage_change


# The sectoral percentage changes in global GHG emissions have been successfully computed:
# 
# Key Observations:
# 
#     ## 1990 to 2005:
#         Power Industry emissions increased by 40.4%.
#         Industrial Combustion emissions increased by 20.5%.
#         Transport emissions increased by 40.0%.
# 
#     ## 2005 to 2022:
#         Power Industry emissions grew 29.9%.
#         Processes emissions grew 51.6%.
#         Waste emissions increased by 30.9%.
# 
#     ## 2022 to 2023:
#         Most sectors saw a small increase (~1-3%).

# In[ ]:





# # EU27

# In[75]:


# Filter data for EU27
df_eu27 = df_ghg_sector[df_ghg_sector["Country"] == "EU27"]

# Summarize EU27 emissions by sector for each year
df_eu27_sector = df_eu27.drop(columns=["EDGAR Country Code", "Country", "Substance"]).groupby("Sector").sum()

# Transpose the dataframe for better readability
df_eu27_transposed = df_eu27_sector.T

# Define years of interest for EU27 visualization
years_reference_eu27 = [1990, 2005, 2022, 2023]

# Compute percentage changes
df_eu27_changes = df_eu27_transposed.loc[years_reference_eu27].pct_change() * 100

# Round values for better readability
df_eu27_changes = df_eu27_changes.round(1)

# Display the EU27 percentage changes
df_eu27_changes


# ### EU27 GHG Emissions Percentage Changes:
# 
#     1990 to 2005:
#         Agriculture emissions decreased by -21.9%.
#         Power Industry emissions slightly decreased by -1.9%.
#         Transport emissions increased by 27.2%.
# 
#     2005 to 2022:
#         Power Industry emissions saw a -37.7% decline.
#         Buildings emissions dropped -27.3%.
#         Waste emissions decreased by -24.5%.
# 
#     2022 to 2023:
#         Minimal changes in most sectors (-1% to -8%).
#         Transport emissions slightly declined by -1.8%.

# In[ ]:





# In[76]:


# Define years of interest for EU27 visualization
years_to_plot_eu27 = [1990, 2005, 2015, 2023]

# Filter the dataset for the selected years
df_eu27_plot = df_eu27_transposed.loc[years_to_plot_eu27]

# Plot the stacked bar chart for EU27
df_eu27_plot.plot(kind='bar', stacked=True, figsize=(12, 6), colormap='tab10')
plt.title("EU27 GHG Emissions by Sector (Selected Years)")
plt.xlabel("Year")
plt.ylabel("Mt CO₂eq")
plt.legend(title="Sector", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Show the plot
plt.show()


# The stacked bar chart successfully visualizes EU27 GHG emissions by sector for the selected years (1990, 2005, 2015, 2023). The decline in emissions across sectors is clearly visible, particularly in Power Industry, Industrial Combustion, and Waste.

# In[ ]:





# In[77]:


# Step 1: Define a specific color mapping for sectors (based on your reference image)
sector_colors = {
    "Power Industry": "#6441A5",  # Purple
    "Industrial Combustion": "#FF3366",  # Red
    "Buildings": "#FF8000",  # Orange
    "Transport": "#FF99CC",  # Light Pink
    "Fuel Exploitation": "#00A86B",  # Green
    "Agriculture": "#1E90FF",  # Blue
    "Waste": "#808080",  # Grey
    "Processes": "#8B4513"  # Brown
}

# Step 2: Extract all years for EU27 emissions by sector
years_range = list(range(1990, 2024))  # From 1990 to 2023
eu27_emissions_by_sector = eu27_data[["Sector"] + years_range]

# Step 3: Sum emissions for each sector over the years
sector_emissions_over_time_full = eu27_emissions_by_sector.groupby("Sector").sum()

# Step 4: Generate the stacked bar chart with **custom colors**
plt.figure(figsize=(14, 7))
sector_emissions_over_time_full.T.plot(
    kind="bar", 
    stacked=True, 
    figsize=(14, 7), 
    width=0.8, 
    color=[sector_colors[sector] for sector in sector_emissions_over_time_full.index], 
    legend=True
)

plt.xlabel("Year")
plt.ylabel("GHG Emissions (Mt CO2eq)")
plt.title("EU27 GHG Emissions by Sector (1990-2023)")
plt.xticks(rotation=45)
plt.legend(title="Sector", bbox_to_anchor=(1.05, 1), loc="upper left")

# Show the updated stacked bar chart with **correct colors**
plt.show()


# In[80]:


# Load the newly uploaded Excel file to double-check structure
xls_new = pd.ExcelFile("EDGAR_2024_GHG_booklet_2024(1).xlsx")

# List all sheet names to find the right one
sheet_names_new = xls_new.sheet_names

# Preview the first few rows from each sheet to understand structure
sheet_previews_new = {sheet: xls_new.parse(sheet).head() for sheet in sheet_names_new}

sheet_names_new, sheet_previews_new


# In[84]:


# Load the correct sheet
df_sector_fixed = xls_new.parse("GHG_by_sector_and_country")

# Step 1: Clean up column names (strip whitespace)
df_sector_fixed.columns = df_sector_fixed.columns.map(lambda x: str(x).strip() if isinstance(x, str) else x)

# Step 2: Use 2023 as an integer column (not string)
year_col = 2023

# Step 3: Filter for EU27 data and valid values in 2023
eu27_only = df_sector_fixed[df_sector_fixed["Country"].str.strip() == "EU27"]
eu27_emissions_by_substance = eu27_only[eu27_only[year_col].notna()]

# Step 4: Aggregate by substance
substance_emissions_2023 = eu27_emissions_by_substance.groupby("Substance")[year_col].sum().reset_index()

# Step 5: Calculate percentage
total_ghg_2023 = substance_emissions_2023[year_col].sum()
substance_emissions_2023["Percentage (%)"] = (substance_emissions_2023[year_col] / total_ghg_2023) * 100

# Step 6: Label mapping and color scheme
substance_colors = {
    "CO2": "#336699",
    "GWP_100_AR5_CH4": "#66A3FF",
    "GWP_100_AR5_N2O": "#99CCFF",
    "GWP_100_AR5_F-gases": "#CCE5FF"
}
ghg_labels = {
    "CO2": "CO2",
    "GWP_100_AR5_CH4": "CH4",
    "GWP_100_AR5_N2O": "N2O",
    "GWP_100_AR5_F-gases": "F-gases"
}
substance_emissions_2023["Substance Label"] = substance_emissions_2023["Substance"].map(ghg_labels)

# Step 7: Plot pie chart
plt.figure(figsize=(6, 6))
plt.pie(
    substance_emissions_2023["Percentage (%)"],
    labels=substance_emissions_2023["Substance Label"],
    autopct="%1.1f%%",
    startangle=140,
    colors=[substance_colors.get(sub, "#336699") for sub in substance_emissions_2023["Substance"]],
    wedgeprops={"edgecolor": "white", "linewidth": 1}
)
plt.title("GHG % in 2023 (EU27)", fontsize=12, fontweight="bold")
plt.show()

# Step 8: Display the table
print("\nGHG Substance Breakdown for EU27 in 2023:")
print(substance_emissions_2023[["Substance Label", "Percentage (%)"]])



# In[ ]:





# In[85]:


# Step 1: Extract emissions for EU27 by sector for relevant years (1990, 2005, 2022, 2023)
comparison_years = [1990, 2005, 2022, 2023]
eu27_sector_comparison = eu27_data[["Sector"] + comparison_years]

# Step 2: Sum emissions for each sector over selected years
sector_emissions_comparison = eu27_sector_comparison.groupby("Sector").sum()

# Step 3: Compute percentage changes for each sector
percentage_changes = sector_emissions_comparison.copy()

for year_pair in [(2023, 1990), (2023, 2005), (2023, 2022)]:
    year_1, year_2 = year_pair
    column_name = f"{year_1} vs {year_2} (%)"
    percentage_changes[column_name] = (
        (sector_emissions_comparison[year_1] - sector_emissions_comparison[year_2])
        / sector_emissions_comparison[year_2]
    ) * 100

# Step 4: Format the results into a structured table
formatted_table_no_ace = percentage_changes[["2023 vs 1990 (%)", "2023 vs 2005 (%)", "2023 vs 2022 (%)"]].reset_index()

# Function to format percentage change values with arrows
def format_percentage(value):
    if value > 0:
        return f"\033[91m↗ +{value:.1f}%\033[0m"  # Red upward arrow for increase
    elif value < 0 and value > -2:
        return f"\033[93m→ {value:.1f}%\033[0m"  # Yellow side arrow for small decreases (close to 0)
    elif value < -2:
        return f"\033[92m↘ {value:.1f}%\033[0m"  # Green downward arrow for significant decreases
    else:
        return f"\033[93m→ {value:.1f}%\033[0m"  # Yellow arrow for exact zero change

# Apply formatting to the percentage change columns
for col in ["2023 vs 1990 (%)", "2023 vs 2005 (%)", "2023 vs 2022 (%)"]:
    formatted_table_no_ace[col] = formatted_table_no_ace[col].apply(format_percentage)

# Step 5: Sort the table in ascending order by the "2023 vs 1990 (%)" column
formatted_table_no_ace_sorted = formatted_table_no_ace.sort_values(by="2023 vs 1990 (%)", ascending=True)

# Display the final formatted table without ace_tools
print("\n\033[1mEU27 GHG Emissions Trends with Colored Arrows (Sorted in Ascending Order)\033[0m")
print(formatted_table_no_ace_sorted.to_string(index=False))


# In[ ]:





# In[86]:


# Step 1: Extract emissions for EU27 by sector for relevant years (1990, 2005, 2022, 2023)
comparison_years = [1990, 2005, 2022, 2023]
eu27_sector_comparison = eu27_data[["Sector"] + comparison_years]

# Step 2: Sum emissions for each sector over selected years
sector_emissions_comparison = eu27_sector_comparison.groupby("Sector").sum()

# Step 3: Compute percentage changes for each sector and round off values
percentage_changes = sector_emissions_comparison.copy()

for year_pair in [(2023, 1990), (2023, 2005), (2023, 2022)]:
    year_1, year_2 = year_pair
    column_name = f"{year_1} vs {year_2} (%)"
    percentage_changes[column_name] = (
        (sector_emissions_comparison[year_1] - sector_emissions_comparison[year_2])
        / sector_emissions_comparison[year_2]
    ) * 100
    percentage_changes[column_name] = percentage_changes[column_name].round(0)  # Round to whole numbers

# Step 4: Format the results into a structured table
formatted_table_no_ace = percentage_changes[["2023 vs 1990 (%)", "2023 vs 2005 (%)", "2023 vs 2022 (%)"]].reset_index()

# Function to format percentage change values with arrows
def format_percentage(value):
    if value > 0:
        return f"\033[91m↗ +{int(value)}%\033[0m"  # Red upward arrow for increase
    elif value < 0 and value > -2:
        return f"\033[93m→ {int(value)}%\033[0m"  # Yellow side arrow for small decreases (close to 0)
    elif value < -2:
        return f"\033[92m↘ {int(value)}%\033[0m"  # Green downward arrow for significant decreases
    else:
        return f"\033[93m→ {int(value)}%\033[0m"  # Yellow arrow for exact zero change

# Apply formatting to the percentage change columns
for col in ["2023 vs 1990 (%)", "2023 vs 2005 (%)", "2023 vs 2022 (%)"]:
    formatted_table_no_ace[col] = formatted_table_no_ace[col].apply(format_percentage)

# Step 5: Sort the table in ascending order by the "2023 vs 1990 (%)" column
formatted_table_no_ace_sorted = formatted_table_no_ace.sort_values(by="2023 vs 1990 (%)", ascending=True)

# Display the final formatted table without ace_tools
print("\n\033[1mEU27 GHG Emissions Trends with Colored Arrows (Sorted in Ascending Order)\033[0m")
print(formatted_table_no_ace_sorted.to_string(index=False))


# In[ ]:





# ### **Python Code to Calculate EU27 GHG Emissions Table**
# This code **automatically computes**:
# 1. **Total GHG emissions** for EU27 by summing all sector emissions.
# 2. **GHG emissions per capita** using:
# 
#    \[
#    \text{GHG per Capita} = \frac{\text{Total GHG Emissions} \times 10^6}{\text{Population}}
#    \]
#    
# 3. **GHG emissions per unit of GDP** using:
# 
#    \[
#    \text{GHG per GDP} = \frac{\text{Total GHG Emissions}}{\text{GDP (PPP in Trillions)} \div 1000}
#    \]
#    
# 4. **Population and GDP values** (taken from the image).
# 
# ---
# 
# ### **Final Output Table**
# | **Year** | **GHG Emissions (Mt CO₂eq/yr)** | **Population** | **GHG per Capita (t CO₂eq/cap/yr)** | **GHG per GDP (t CO₂eq/kUSD/yr)** |
# |---------|--------------------------------|-------------|--------------------------------|--------------------------------|
# | **1990** | **4877.28** | **420.198M** | **11.607** | **0.343** |
# | **2005** | **4553.56** | **435.163M** | **10.464** | **0.239** |
# | **2015** | **3879.73** | **442.095M** | **8.776** | **0.183** |
# | **2023** | **3221.79** | **443.523M** | **7.264** | **0.133** |
# 
# 

# In[89]:


# Step 1: Extract total GHG emissions for EU27 for the required years (1990, 2005, 2015, 2023)
selected_years = [1990, 2005, 2015, 2023]
ghg_total_emissions = eu27_data[["Country"] + selected_years]

# Step 2: Sum emissions across all sectors for each year
ghg_total_emissions = ghg_total_emissions.drop(columns=["Country"]).sum().reset_index()
ghg_total_emissions.columns = ["Year", "GHG Emissions (Mt CO2eq/yr)"]

# Step 3: Add Population data (as extracted from the provided image)
population_values = {
    1990: 420.198e6,  # Convert from million to absolute numbers
    2005: 435.163e6,
    2015: 442.095e6,
    2023: 443.523e6
}
ghg_total_emissions["Population"] = ghg_total_emissions["Year"].map(population_values)

# Step 4: Compute GHG emissions per capita using the formula:
# GHG per Capita (t CO2eq/cap/yr) = (Total GHG Emissions * 1e6) / Population
ghg_total_emissions["GHG Emissions per Capita (t CO2eq/cap/yr)"] = (
    ghg_total_emissions["GHG Emissions (Mt CO2eq/yr)"] * 1e6 / ghg_total_emissions["Population"]
).round(3)

# Step 5: Add GDP data (from reference image)
gdp_values = {
    1990: 14.22e6,  # Convert from Trillion to Million USD (kUSD)
    2005: 19.05e6,
    2015: 21.2e6,
    2023: 24.2e6
}
ghg_total_emissions["GDP (Million USD)"] = ghg_total_emissions["Year"].map(gdp_values)

# Step 6: Compute GHG emissions per GDP using the corrected formula:
# GHG per GDP (t CO2eq/kUSD/yr) = (Total GHG Emissions * 1e3) / GDP (Million USD)
ghg_total_emissions["GHG Emissions per unit of GDP PPP (t CO2eq/kUSD/yr)"] = (
    ghg_total_emissions["GHG Emissions (Mt CO2eq/yr)"] * 1e3 / ghg_total_emissions["GDP (Million USD)"]
).round(3)

# Step 7: Convert Population to millions for readability
ghg_total_emissions["Population"] = (ghg_total_emissions["Population"] / 1e6).round(3).astype(str) + "M"

# Step 8: Remove the extra GDP column (if not needed)
ghg_total_emissions = ghg_total_emissions.drop(columns=["GDP (Million USD)"])

# Step 9: Print the final table
print("\nEU27 GHG Emissions Table with Calculated Values:\n")
print(ghg_total_emissions.to_string(index=False))


# In[ ]:





# ### **Solution for Calculating Each Value in the EU27 GHG Emissions Table**
# The **GHG emissions table** is calculated using the following formulas:
# 
# ---
# 
# ### **1. GHG Emissions (Mt CO₂eq/yr)**
# **Extracted from the dataset**, summing emissions across all sectors for the years **1990, 2005, 2015, and 2023**.
# 
# ---
# 
# ### **2. Population**
# The **population values** were extracted from the **image** and converted into absolute numbers:
# 
# | **Year** | **Population (Millions)** |
# |----------|---------------------------|
# | **1990** | **420.198M** |
# | **2005** | **435.163M** |
# | **2015** | **442.095M** |
# | **2023** | **443.523M** |
# 
# ---
# 
# ### **3. GHG Emissions per Capita (t CO₂eq/cap/yr)**
# \[
# \text{GHG per Capita} = \frac{\text{Total GHG Emissions} \times 10^6}{\text{Population}}
# \]
# 
# - **Example for 1990:**
#   \[
#   \frac{4877.28 \times 10^6}{420.198 \times 10^6} = 11.607 \text{ t CO₂eq/cap/yr}
#   \]
# 
# - **Example for 2023:**
#   \[
#   \frac{3221.79 \times 10^6}{443.523 \times 10^6} = 7.264 \text{ t CO₂eq/cap/yr}
#   \]
# 
# ---
# 
# ### **4. GHG Emissions per Unit of GDP PPP (t CO₂eq/kUSD/yr)**
# \[
# \text{GHG per GDP} = \frac{\text{Total GHG Emissions}}{\text{GDP (PPP in Trillions)} \div 1000}
# \]
# 
# **GDP values (in Trillions of USD):**
# | **Year** | **GDP (PPP) in Trillions** |
# |----------|-----------------------------|
# | **1990** | **14.22** |
# | **2005** | **19.05** |
# | **2015** | **21.2** |
# | **2023** | **24.2** |
# 
# - **Example for 1990:**
#   \[
#   \frac{4877.28}{14.22 \times 1000} = 0.343 \text{ t CO₂eq/kUSD/yr}
#   \]
# 
# - **Example for 2023:**
#   \[
#   \frac{3221.79}{24.2 \times 1000} = 0.133 \text{ t CO₂eq/kUSD/yr}
#   \]
# 
# ---
# 
# ### **Final Table Output:**
# | **Year** | **GHG Emissions (Mt CO₂eq/yr)** | **Population** | **GHG per Capita (t CO₂eq/cap/yr)** | **GHG per GDP (t CO₂eq/kUSD/yr)** |
# |----------|--------------------------------|-------------|--------------------------------|--------------------------------|
# | **1990** | **4877.28** | **420.198M** | **11.607** | **0.343** |
# | **2005** | **4553.56** | **435.163M** | **10.464** | **0.239** |
# | **2015** | **3879.73** | **442.095M** | **8.776** | **0.183** |
# | **2023** | **3221.79** | **443.523M** | **7.264** | **0.133** |
# 
# 

# 

# In[ ]:





# # INTERNATIONAL SHIPPING

# In[91]:


# Filter data for International Shipping
df_shipping = df_ghg_sector[df_ghg_sector["Country"] == "International Shipping"]

# Summarize emissions by year (all transport-related emissions)
df_shipping_sector = df_shipping.drop(columns=["EDGAR Country Code", "Country", "Substance"]).groupby("Sector").sum()

# Transpose the dataframe for better readability
df_shipping_transposed = df_shipping_sector.T

# Plot the emissions trend for International Shipping
plt.figure(figsize=(12, 6))
plt.bar(df_shipping_transposed.index, df_shipping_transposed["Transport"], color='skyblue', label="Transport Emissions")
plt.title("International Shipping GHG Emissions Over Time")
plt.xlabel("Year")
plt.ylabel("Mt CO₂eq")
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Show the plot
plt.show()


# The bar chart successfully visualizes GHG emissions from International Shipping over time. The emissions show an overall increasing trend from 1970 to 2023, with fluctuations.

# In[92]:


# Check available column names in the International Shipping dataset
available_columns_shipping = df_shipping_transposed.columns.tolist()
available_columns_shipping


# In[93]:


# Check if CO₂, CH₄, and N₂O data exist in the full shipping dataset
df_shipping_transposed.head()


# In[94]:


import pandas as pd

# Load the Excel file
file_path = "EDGAR_2024_GHG_booklet_2024(1).xlsx"
xls = pd.ExcelFile(file_path)

# Display sheet names to identify relevant data
xls.sheet_names


# Load the "GHG_by_sector_and_country" sheet
ghg_sector_data = xls.parse("GHG_by_sector_and_country")

# Display the first few rows to understand the structure
ghg_sector_data.head()


# In[95]:


# Step 1: Extract emissions data for International Shipping in 2023
international_shipping = ghg_sector_data[ghg_sector_data["Country"] == "International Shipping"]

# Step 2: Extract relevant columns (Substance and 2023 emissions)
shipping_emissions_2023 = international_shipping[["Substance", 2023]].rename(columns={2023: "Emissions (Mt CO2eq)"})

# Step 3: Aggregate emissions by substance (sum total emissions for each GHG)
aggregated_shipping_emissions = shipping_emissions_2023.groupby("Substance", as_index=False).sum(numeric_only=True)

# Step 4: Compute total emissions
total_shipping_emissions = aggregated_shipping_emissions["Emissions (Mt CO2eq)"].sum()

# Step 5: Compute percentage contribution for each GHG
aggregated_shipping_emissions["Percentage (%)"] = (aggregated_shipping_emissions["Emissions (Mt CO2eq)"] / total_shipping_emissions) * 100

# Step 6: Define GHG labels for better readability
ghg_labels = {
    "CO2": "CO2",
    "GWP_100_AR5_CH4": "CH4",
    "GWP_100_AR5_N2O": "N2O"
}

# Map the labels to substances
aggregated_shipping_emissions["Substance Label"] = aggregated_shipping_emissions["Substance"].map(ghg_labels)

# Step 7: Display the computed emissions and percentages
print("International Shipping Emissions for 2023:")
print(aggregated_shipping_emissions[["Substance Label", "Emissions (Mt CO2eq)", "Percentage (%)"]])

# Step 8: Generate a pie chart for visualization
import matplotlib.pyplot as plt

plt.figure(figsize=(6,6))
plt.pie(
    aggregated_shipping_emissions["Percentage (%)"], 
    labels=aggregated_shipping_emissions["Substance Label"], 
    autopct='%1.1f%%', 
    startangle=140
)
plt.title("GHG % in International Shipping (2023)")

# Show the chart
plt.show()


# Here is the **International Shipping GHG Emissions for 2023** in table and pie chart format:
# 
# ### Emissions Data:
# | Substance | Emissions (Mt CO₂eq) | Percentage (%) |
# |-----------|----------------------|---------------|
# | CO₂       | 706.32               | 94.56%       |
# | CH₄       | 14.56                | 1.95%        |
# | N₂O       | 26.06                | 3.49%        |
# 
# ### Visualization:
# The pie chart shows the percentage contribution of **CO₂, CH₄, and N₂O** in international shipping.
# 

# In[ ]:





# In[96]:


# Define the years again to ensure they are available
years = [1990, 2005, 2015, 2023]

# Step 1: Extract emissions data for International Shipping
international_shipping_years = ghg_sector_data[ghg_sector_data["Country"] == "International Shipping"]

# Step 2: Select only the relevant year columns
selected_columns = ["Substance"] + years  # Include "Substance" to aggregate correctly
international_shipping_years = international_shipping_years[selected_columns]

# Step 3: Aggregate emissions across substances for each year
emissions_by_year = international_shipping_years.set_index("Substance").sum().reset_index()
emissions_by_year.columns = ["Year", "GHG Emissions (Mt CO2eq/yr)"]

# Step 4: Add placeholder columns for missing data (since GDP and Population data are not available)
emissions_by_year["GHG Emissions per Capita (t CO2eq/cap/yr)"] = "n/a"
emissions_by_year["GHG Emissions per unit of GDP PPP (t CO2eq/kUSD/yr)"] = "n/a"
emissions_by_year["Population"] = "n/a"

# Step 5: Convert to DataFrame and print the table
import pandas as pd

# Create DataFrame
emissions_table = pd.DataFrame(emissions_by_year)

# Print the table
print(emissions_table.to_string(index=False))


# In[97]:


# Sort the table in descending order by Year
emissions_by_year_sorted = emissions_by_year.sort_values(by="Year", ascending=False)

# Convert to DataFrame and print the sorted table
emissions_table_sorted = pd.DataFrame(emissions_by_year_sorted)

# Print the table
print(emissions_table_sorted.to_string(index=False))


# In[ ]:





# Here is the **International Shipping GHG Emissions Over Time** table sorted in **descending order** (latest year first):
# 
# ### **Emissions Data (2023-1990)**
# 
# | Year  | GHG Emissions (Mt CO₂eq/yr) | GHG Emissions per Capita (t CO₂eq/cap/yr) | GHG Emissions per unit of GDP PPP (t CO₂eq/kUSD/yr) | Population |
# |-------|-----------------------------|--------------------------------------------|------------------------------------------------------|------------|
# | 2023  | 746.94                      | n/a                                        | n/a                                                  | n/a        |
# | 2015  | 702.19                      | n/a                                        | n/a                                                  | n/a        |
# | 2005  | 608.74                      | n/a                                        | n/a                                                  | n/a        |
# | 1990  | 395.34                      | n/a                                        | n/a                                                  | n/a        |
# 
# ### **Key Details:**
# - The table is  **sorted in descending order** with **2023 first**.
# - **GHG Emissions (Mt CO₂eq/yr)** were extracted and aggregated for **International Shipping**.
# - **Per capita and GDP-based emissions** are **n/a** due to the absence of population and GDP data.
# 

# In[ ]:





# In[98]:


# Step 1: Extract emissions for International Shipping for relevant years including 2022
comparison_years = [1990, 2005, 2022, 2023]
international_shipping_comparison = ghg_sector_data[ghg_sector_data["Country"] == "International Shipping"][comparison_years]

# Step 2: Sum emissions across all substances for each year
emissions_comparison = international_shipping_comparison.sum().reset_index()
emissions_comparison.columns = ["Year", "GHG Emissions (Mt CO2eq/yr)"]

# Step 3: Convert to dictionary for easier access
emissions_dict = emissions_comparison.set_index("Year")["GHG Emissions (Mt CO2eq/yr)"].to_dict()

# Step 4: Calculate percentage changes
percentage_changes = {
    "2023 vs 1990": ((emissions_dict[2023] - emissions_dict[1990]) / emissions_dict[1990]) * 100,
    "2023 vs 2005": ((emissions_dict[2023] - emissions_dict[2005]) / emissions_dict[2005]) * 100,
    "2023 vs 2022": ((emissions_dict[2023] - emissions_dict[2022]) / emissions_dict[2022]) * 100
}

# Step 5: Create a structured table
percentage_change_table = pd.DataFrame({
    "Comparison": ["2023 vs 1990", "2023 vs 2005", "2023 vs 2022"],
    "Percentage Change (%)": [percentage_changes["2023 vs 1990"], percentage_changes["2023 vs 2005"], percentage_changes["2023 vs 2022"]]
})

# Display the results
print("Percentage Change in International Shipping GHG Emissions:")
print(percentage_change_table.to_string(index=False))


# ### **Steps to Calculate Percentage Change:**
# For each pair of years:
# \[
# \text{Percentage Change} = \left( \frac{\text{Emissions in 2023} - \text{Emissions in Previous Year}}{\text{Emissions in Previous Year}} \right) \times 100
# \]
# 
# ### **Comparisons Required:**
# 1. **2023 vs 1990:** 
#    \[
#    \left( \frac{\text{Emissions in 2023} - \text{Emissions in 1990}}{\text{Emissions in 1990}} \right) \times 100
#    \]
# 2. **2023 vs 2005:** 
#    \[
#    \left( \frac{\text{Emissions in 2023} - \text{Emissions in 2005}}{\text{Emissions in 2005}} \right) \times 100
#    \]
# 3. **2023 vs 2022:** 
#    - First, extract **2022 emissions** from the dataset.
#    - Compute percentage change:
#    \[
#    \left( \frac{\text{Emissions in 2023} - \text{Emissions in 2022}}{\text{Emissions in 2022}} \right) \times 100
#    \]
# 
# I will now compute these percentage changes for **International Shipping** emissions.
# 
# ### **Percentage Change in International Shipping GHG Emissions**
# This table represents the **growth in emissions** over different time periods:
# 
# | **Comparison**  | **Percentage Change (%)** |
# |----------------|--------------------------|
# | **2023 vs 1990** | **+88.94%** |
# | **2023 vs 2005** | **+22.70%** |
# | **2023 vs 2022** | **+1.07%** |
# 
# ### **How We Computed This:**
# For each comparison:
# \[
# \text{Percentage Change} = \left( \frac{\text{Emissions in 2023} - \text{Emissions in Previous Year}}{\text{Emissions in Previous Year}} \right) \times 100
# \]
# 
# - **+88.94% increase** in emissions from **1990 to 2023**.
# - **+22.70% increase** from **2005 to 2023**.
# - **+1.07% increase** from **2022 to 2023**.

# In[ ]:





# # INTERNATIONAL AVIATION

# In[99]:


# Filter data for International Aviation
df_aviation = df_ghg_sector[df_ghg_sector["Country"] == "International Aviation"]

# Summarize emissions by year (all transport-related emissions)
df_aviation_sector = df_aviation.drop(columns=["EDGAR Country Code", "Country", "Substance"]).groupby("Sector").sum()

# Transpose the dataframe for better readability
df_aviation_transposed = df_aviation_sector.T

# Plot the emissions trend for International Aviation
plt.figure(figsize=(12, 6))
plt.bar(df_aviation_transposed.index, df_aviation_transposed["Transport"], color='blue', label="Transport Emissions")
plt.title("International Aviation GHG Emissions Over Time")
plt.xlabel("Year")
plt.ylabel("Mt CO₂eq")
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Show the plot
plt.show()


# The bar chart successfully visualizes GHG emissions from International Aviation over time. The emissions steadily increased until a sharp decline in 2020, likely due to the COVID-19 pandemic, followed by a recovery.

# In[111]:


# Display the actual GHG emissions by year for the Transport sector (International Aviation)
print("\nInternational Aviation GHG Emissions by Year (Mt CO2eq):")
print(df_aviation_transposed["Transport"])


# In[112]:


aviation_2023 = df_aviation_transposed.loc[2023, "Transport"]
print(f"International Aviation GHG in 2023: {aviation_2023:.2f} Mt CO₂eq")


# In[ ]:





# In[100]:


# Define reference years for percentage change calculations
years_reference_shipping_aviation = [1990, 2005, 2022, 2023]

# Compute percentage changes for International Shipping
df_shipping_changes = df_shipping_transposed.loc[years_reference_shipping_aviation].pct_change() * 100

# Compute percentage changes for International Aviation
df_aviation_changes = df_aviation_transposed.loc[years_reference_shipping_aviation].pct_change() * 100

# Round values for better readability
df_shipping_changes = df_shipping_changes.round(1)
df_aviation_changes = df_aviation_changes.round(1)

# Display the results
df_shipping_changes, df_aviation_changes


# Sectoral Percentage Changes for International Shipping & Aviation:
# 
# International Shipping:
# 
#     1990 to 2005:
#         Fuel Exploitation: +44.6%
#         Processes: +53.8%
#         Transport: +54.2%
# 
#     2005 to 2022:
#         Fuel Exploitation: -5.9%
#         Processes: +22.4%
#         Transport: +22.0%
# 
#     2022 to 2023:
#         Minimal increases (~1%) across all sectors.

# International Aviation:
# 
#     1990 to 2005:
#         Processes: +54.6%
#         Transport: +64.6%
# 
#     2005 to 2022:
#         Processes & Transport saw a small decline (~-4.1%).
# 
#     2022 to 2023:
#         Processes & Transport rebounded (+19.5%).

# In[102]:


# Recompute transposed datasets for International Shipping and Aviation
df_shipping_transposed_fixed = df_shipping_sector.T
df_aviation_transposed_fixed = df_aviation_sector.T

# Check available years after ensuring the correct structure
available_years_shipping = df_shipping_transposed_fixed.index
available_years_aviation = df_aviation_transposed_fixed.index

# Display available years to verify correct indexing
available_years_shipping, available_years_aviation




# In[104]:


# Ensure the index is of integer type for proper alignment
df_shipping_transposed_fixed.index = df_shipping_transposed_fixed.index.astype(int)
df_aviation_transposed_fixed.index = df_aviation_transposed_fixed.index.astype(int)

# Define the reference years again (ensuring they match the dataset)
years_reference_fixed = [1990, 2005, 2022, 2023]

# Compute percentage changes for International Shipping (corrected)
df_shipping_changes_fixed = df_shipping_transposed_fixed.loc[years_reference_fixed].pct_change() * 100

# Compute percentage changes for International Aviation (corrected)
df_aviation_changes_fixed = df_aviation_transposed_fixed.loc[years_reference_fixed].pct_change() * 100

# Round values for better readability
df_shipping_changes_fixed = df_shipping_changes_fixed.round(1)
df_aviation_changes_fixed = df_aviation_changes_fixed.round(1)

# Display the corrected percentage change tables
df_shipping_changes_fixed, df_aviation_changes_fixed


# In[105]:


# Formatting the percentage change data into structured tables
import pandas as pd

# Create tables for International Shipping and Aviation
df_shipping_changes_fixed.insert(0, "Sector", "International Shipping")
df_aviation_changes_fixed.insert(0, "Sector", "International Aviation")

# Reset index to properly label the years
df_shipping_changes_fixed.reset_index(inplace=True)
df_aviation_changes_fixed.reset_index(inplace=True)

# Rename index column to "Year"
df_shipping_changes_fixed.rename(columns={"index": "Year"}, inplace=True)
df_aviation_changes_fixed.rename(columns={"index": "Year"}, inplace=True)

# Concatenate both tables for a single structured view
df_sector_changes = pd.concat([df_shipping_changes_fixed, df_aviation_changes_fixed])

# Display the formatted table
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 4))
ax.axis('tight')
ax.axis('off')
table_data = df_sector_changes.values.tolist()
columns = df_sector_changes.columns.tolist()

# Create a table plot
table = ax.table(cellText=table_data, colLabels=columns, cellLoc='center', loc='center')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.auto_set_column_width([i for i in range(len(columns))])

# Show the table
plt.show()


# In[106]:


# Reconstruct df_aviation_table from the corrected dataset with the Year column included
years_reference_aviation = [1990, 2005, 2015, 2023]

# Extract relevant years from the transposed dataset
df_aviation_selected = df_aviation_transposed.loc[years_reference_aviation]

# Compute total GHG emissions per year by summing all substances
df_aviation_table = pd.DataFrame({
    "Year": df_aviation_selected.index,  # Ensure Year is included as a column
    "GHG emissions (Mt CO₂eq/yr)": df_aviation_selected.sum(axis=1),  # Summing all emissions
    "GHG emissions per capita (t CO₂eq/cap/yr)": ["n/a"] * len(df_aviation_selected),
    "GHG emissions per unit of GDP PPP (t CO₂eq/kUSD/yr)": ["n/a"] * len(df_aviation_selected),
    "Population": ["n/a"] * len(df_aviation_selected)
})

# Display the formatted table with the Year column
fig, ax = plt.subplots(figsize=(8, 2))
ax.axis('tight')
ax.axis('off')

# Extract data and columns for table display
table_data = df_aviation_table.values.tolist()
columns = df_aviation_table.columns.tolist()

# Create a structured table plot
table = ax.table(cellText=table_data, colLabels=columns, cellLoc='center', loc='center')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.auto_set_column_width([i for i in range(len(columns))])

# Show the final table with the Year column
plt.show()


# In[108]:


# Reconstruct df_aviation_table with the Year column and sort in descending order
df_aviation_table_sorted = df_aviation_table.sort_values(by="Year", ascending=False)

# Display the formatted International Aviation table with the Year column in descending order
fig, ax = plt.subplots(figsize=(8, 2))
ax.axis('tight')
ax.axis('off')

# Extract data and columns for table display
table_data = df_aviation_table_sorted.values.tolist()
columns = df_aviation_table_sorted.columns.tolist()

# Create a structured table plot
table = ax.table(cellText=table_data, colLabels=columns, cellLoc='center', loc='center')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.auto_set_column_width([i for i in range(len(columns))])

# Show the final table with the Year column sorted in descending order
plt.show()


# In[110]:


# Check the column names and structure of df_aviation
df_aviation.head()


# In[109]:


# Extract sectoral emissions for International Aviation for the required years
df_aviation_sector_selected = df_aviation_transposed.loc[[1990, 2005, 2015, 2023]]

# Plot the stacked bar chart for GHG emissions by sector in International Aviation
df_aviation_sector_selected.plot(kind='bar', stacked=True, figsize=(10, 5), colormap='tab10')

# Customize the chart
plt.title("International Aviation GHG Emissions by Sector (1990-2023)", fontsize=14, fontweight="bold")
plt.xlabel("Year", fontsize=12)
plt.ylabel("Mt CO₂eq", fontsize=12)
plt.xticks(rotation=0)
plt.legend(title="Sector", bbox_to_anchor=(1.05, 1), loc='upper left')

# Show the final stacked bar chart
plt.show()


# In[ ]:





# In[107]:


# Extract total emissions for International Aviation for the required years (ensuring correct indexing)
df_aviation_selected_fixed = df_aviation_transposed.loc[[1990, 2005, 2022, 2023]]

# Compute percentage changes based on total emissions
aviation_changes = {
    "2023 vs 1990": ((df_aviation_selected_fixed.loc[2023].sum() - df_aviation_selected_fixed.loc[1990].sum()) / df_aviation_selected_fixed.loc[1990].sum()) * 100,
    "2023 vs 2005": ((df_aviation_selected_fixed.loc[2023].sum() - df_aviation_selected_fixed.loc[2005].sum()) / df_aviation_selected_fixed.loc[2005].sum()) * 100,
    "2023 vs 2022": ((df_aviation_selected_fixed.loc[2023].sum() - df_aviation_selected_fixed.loc[2022].sum()) / df_aviation_selected_fixed.loc[2022].sum()) * 100
}

# Convert to a DataFrame for easier visualization
df_aviation_changes = pd.DataFrame(aviation_changes, index=["International Aviation"]).round(1)

# Display the formatted percentage change table
fig, ax = plt.subplots(figsize=(6, 2))
ax.axis('tight')
ax.axis('off')

# Extract data and columns for table display
table_data = df_aviation_changes.values.tolist()
columns = df_aviation_changes.columns.tolist()

# Create a structured table plot
table = ax.table(cellText=table_data, colLabels=columns, rowLabels=df_aviation_changes.index, 
                 cellLoc='center', loc='center')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.auto_set_column_width([i for i in range(len(columns))])

# Show the final table with computed percentage changes
plt.show()


# In[117]:


# Step 1: Extract substance-wise emissions for International Aviation in 2023
year_col = 2023  # Ensure correct column format
df_aviation_substance = df_aviation[df_aviation[year_col].notna()]

# Step 2: Aggregate emissions by substance
substance_emissions_2023 = df_aviation_substance.groupby("Substance")[year_col].sum().reset_index()

# Step 3: Compute percentage for each substance
total_ghg_2023 = substance_emissions_2023[year_col].sum()
substance_emissions_2023["Percentage (%)"] = (substance_emissions_2023[year_col] / total_ghg_2023) * 100

# Step 4: Define a color scheme
substance_colors = {
    "CO2": "#336699",
    "GWP_100_AR5_CH4": "#66A3FF",
    "GWP_100_AR5_N2O": "#99CCFF",
    "GWP_100_AR5_F-gases": "#CCE5FF"
}

# Step 5: Map substance names to readable labels
ghg_labels = {
    "CO2": "CO2",
    "GWP_100_AR5_CH4": "CH4",
    "GWP_100_AR5_N2O": "N2O",
    "GWP_100_AR5_F-gases": "F-gases"
}
substance_emissions_2023["Substance Label"] = substance_emissions_2023["Substance"].map(ghg_labels)

# Step 6: Generate the pie chart
plt.figure(figsize=(6, 6))
plt.pie(
    substance_emissions_2023["Percentage (%)"],
    labels=substance_emissions_2023["Substance Label"],
    autopct="%1.1f%%",
    startangle=140,
    colors=[substance_colors.get(sub, "#336699") for sub in substance_emissions_2023["Substance"]],
    wedgeprops={"edgecolor": "white", "linewidth": 1}
)
plt.title("International Aviation GHG Breakdown (2023)", fontsize=12, fontweight="bold")

# Show the pie chart
plt.show()

# Step 7: Display computed percentages
print("\nInternational Aviation GHG Breakdown (2023):")
print(substance_emissions_2023[["Substance Label", "Percentage (%)"]])


# In[ ]:





# In[122]:


# Step 1: Extract emissions for International Aviation in 2023
year_col = 2023  # Ensure correct year column

# Ensure dataset is correctly filtered
df_aviation_ghg_2023 = df_aviation[df_aviation[year_col].notna()].groupby("Substance")[year_col].sum()

# Step 2: Rename substances
ghg_labels = {
    "CO2": "CO2",
    "GWP_100_AR5_CH4": "CH4",
    "GWP_100_AR5_N2O": "N2O"
}

df_aviation_ghg_2023_fixed = df_aviation_ghg_2023.rename(index=ghg_labels)

# Step 3: Normalize emissions to sum to 100%
total_percentage = df_aviation_ghg_2023_fixed.sum()
df_aviation_ghg_2023_normalized = (df_aviation_ghg_2023_fixed / total_percentage) * 100

# Step 4: Extract values and labels
values_normalized = df_aviation_ghg_2023_normalized.values
formatted_labels_normalized = [f"{label} {value:.1f}%" for label, value in zip(df_aviation_ghg_2023_normalized.index, values_normalized)]

# Step 5: Define colors (blue for CO2, white for CH4 and N2O)
colors_fixed = ["#1f77b4", "#ffffff", "#ffffff"]

# Step 6: Create improved pie chart
plt.figure(figsize=(6, 6))

wedges, texts = plt.pie(
    values_normalized, labels=formatted_labels_normalized, startangle=180, colors=colors_fixed,
    textprops={'fontsize': 14, 'color': 'black'}, explode=[0, 0, 0], pctdistance=0.75, labeldistance=1.3,
    wedgeprops={'edgecolor': 'black', 'linewidth': 1.5}  # Improve contrast
)

# Step 7: Adjust label spacing for better readability
for text in texts:
    text.set_fontsize(13)  # Increase font size for labels

# Step 8: Add a bold title
plt.title("International Aviation GHG % in 2023", fontsize=14, fontweight="bold")

# Step 9: Keep the pie centered and circular
plt.axis('equal')

# Step 10: Show the final improved pie chart
plt.show()


# In[123]:


# Recompute the aviation GHG dataset with proper renaming
ghg_labels = {
    "CO2": "CO2",
    "GWP_100_AR5_CH4": "CH4",
    "GWP_100_AR5_N2O": "N2O"
}

# Ensure we extract the correct data again
df_aviation_ghg_2023_fixed = df_aviation_ghg_2023.rename(index=ghg_labels)

# Recalculate total emissions to normalize
total_percentage = df_aviation_ghg_2023_fixed.sum()

# Normalize emissions to sum to 100%
df_aviation_ghg_2023_normalized = (df_aviation_ghg_2023_fixed / total_percentage) * 100

# Extract the new values and labels
values_normalized = df_aviation_ghg_2023_normalized.values
formatted_labels_normalized = [f"{label} {value:.1f}%" for label, value in zip(df_aviation_ghg_2023_normalized.index, values_normalized)]

# Define colors (blue for CO2, white for CH4 and N2O)
colors_fixed = ["#1f77b4", "#ffffff", "#ffffff"]  

# Create the corrected pie chart with normalized percentages
plt.figure(figsize=(5, 5))  # Keep square for circular shape

wedges, texts = plt.pie(
    values_normalized, labels=formatted_labels_normalized, startangle=180, colors=colors_fixed,
    textprops={'fontsize': 12, 'color': 'black'}, explode=[0, 0, 0], pctdistance=0.75, labeldistance=1.2,
    wedgeprops={'edgecolor': 'black', 'linewidth': 1.5}  # Improve contrast on white slices
)

# Adjust text properties for better readability
for text in texts:
    text.set_fontsize(11)  # Label font size

# Add bold title
plt.title("GHG % in 2023", fontsize=12, fontweight="bold")

# Keep the pie centered and circular
plt.axis('equal')  # Ensures the pie remains a perfect circle

# Show the final corrected pie chart
plt.show()


# In[ ]:




