import pandas as pd
import glob

csv_files = glob.glob('data/*.csv')
df_list = [pd.read_csv(f) for f in csv_files]
df = pd.concat(df_list, ignore_index=True)

# Normalize column names
df.columns = df.columns.str.strip().str.lower()

# Filter for 'pink morsel' (singular, as in your data)
df = df[df['product'].str.strip().str.lower() == 'pink morsel']

# Remove $ sign and any commas, then convert to float
df['price'] = df['price'].str.replace(r'[\$,]', '', regex=True)
df['price'] = pd.to_numeric(df['price'], errors='coerce')

# Calculate sales
df['sales'] = df['quantity'] * df['price']

# Select and rename fields
output_df = df[['sales', 'date', 'region']].rename(columns={'date': 'Date', 'region': 'Region'})

# Save to CSV
output_df.to_csv('formatted_sales.csv', index=False)
