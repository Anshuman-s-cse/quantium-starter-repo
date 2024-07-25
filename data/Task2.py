import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
file_path = 'daily_sales_data_0.csv'
sales_data = pd.read_csv(file_path)

# Strip any leading/trailing spaces from column names
sales_data.columns = sales_data.columns.str.strip()

# Print column names and first few rows to inspect the data
print(sales_data.columns)
print(sales_data.head())

# Filter data for Pink Morsels using the correct column name
if 'product' in sales_data.columns:
    pink_morsels = sales_data[sales_data['product'] == 'pink morsel']
else:
    raise KeyError("The 'product' column is not found in the DataFrame.")

# Convert 'date' column to datetime
pink_morsels['date'] = pd.to_datetime(pink_morsels['date'])

# Split data into before and after the price increase
before_increase = pink_morsels[pink_morsels['date'] < '2021-01-15']
after_increase = pink_morsels[pink_morsels['date'] >= '2021-01-15']

# Calculate total sales before and after the price increase
# Assuming 'quantity' represents the number of items sold
total_sales_before = before_increase['quantity'].sum()
total_sales_after = after_increase['quantity'].sum()

# Visualize the data
sales_summary = pd.DataFrame({
    'Period': ['Before', 'After'],
    'Total Sales': [total_sales_before, total_sales_after]
})

sns.barplot(x='Period', y='Total Sales', data=sales_summary)
plt.title('Total Sales of Pink Morsels Before and After Price Increase')
plt.xlabel('Period')
plt.ylabel('Total Sales')
plt.show()

# Print results
print(f"Total Sales Before Price Increase: {total_sales_before}")
print(f"Total Sales After Price Increase: {total_sales_after}")
