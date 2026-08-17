import pandas as pd

# ==========================================
# Cloud / IT Operations Data Cleaning Script
# ==========================================

# Load the raw dataset
input_file = "cloud_it_operations_raw.csv"
output_file = "cloud_it_operations_cleaned.csv"

df = pd.read_csv(input_file)

print("Original dataset shape:", df.shape)

# Convert Date to proper datetime format
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Remove leading/trailing spaces from text columns
text_columns = [
    "Server_ID",
    "Region",
    "Server_Type",
    "Server_Status"
]

for column in text_columns:
    df[column] = df[column].astype(str).str.strip()

# Define numeric columns
numeric_columns = [
    "CPU_Utilization_Pct",
    "Memory_Utilization_Pct",
    "Disk_Utilization_Pct",
    "Requests_Count",
    "Network_Traffic_MBps",
    "Avg_Response_Time_ms",
    "Error_Count",
    "Incident_Count",
    "Availability_Pct"
]

# Make sure numeric columns contain numeric values
for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# Check missing values
print("\nMissing values after conversion:")
print(df.isnull().sum())

# Remove duplicate records
duplicates_before = df.duplicated().sum()
df = df.drop_duplicates()

print("\nDuplicate rows removed:", duplicates_before)

# Remove rows missing important information
critical_columns = [
    "Date",
    "Server_ID",
    "Region",
    "Server_Type",
    "Server_Status"
]

rows_before = len(df)

df = df.dropna(subset=critical_columns)

rows_removed = rows_before - len(df)

print("Rows removed due to missing critical values:", rows_removed)

# Sort by Date and Server ID
df = df.sort_values(
    ["Date", "Server_ID"]
).reset_index(drop=True)

# Save cleaned dataset
df.to_csv(output_file, index=False)

print("\nCleaning completed successfully!")
print("Cleaned dataset shape:", df.shape)
print("Output file:", output_file)

# Display preview
print("\nCleaned dataset preview:")
print(df.head())

# Display final data types
print("\nFinal data types:")
print(df.dtypes)

