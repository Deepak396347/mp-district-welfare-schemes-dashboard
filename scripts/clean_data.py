import pandas as pd

df = pd.read_csv('mp_district_schemes_raw.csv')
print("Initial Raw Rows:", len(df))

# 1. Remove Duplicate Records
df = df.drop_duplicates()
print("After Removing Duplicates:", len(df))

# 2. Fix Logical Errors (Approved > Applications_Received)
invalid_mask = df['Approved_Count'] > df['Applications_Received']
print("Incorrect Logical Rows Fixed:", invalid_mask.sum())
df.loc[invalid_mask, 'Approved_Count'] = df.loc[invalid_mask, 'Applications_Received'] - df.loc[invalid_mask, 'Pending_Count'] - df.loc[invalid_mask, 'Rejected_Count']
df['Approved_Count'] = df['Approved_Count'].clip(lower=0)

# 3. Handle Missing Values
df['Bottleneck_Reason'] = df['Bottleneck_Reason'].fillna('Under Verification')
df['Fund_Utilized_Lakhs'] = df['Fund_Utilized_Lakhs'].fillna(
    (df['Fund_Allocated_Lakhs'] * (df['Approved_Count'] / df['Applications_Received'])).round(2)
)

# 4. Feature Engineering (Approval % & Utilization %)
df['Approval_Rate_Pct'] = ((df['Approved_Count'] / df['Applications_Received']) * 100).round(2)
df['Fund_Utilization_Pct'] = ((df['Fund_Utilized_Lakhs'] / df['Fund_Allocated_Lakhs']) * 100).round(2)

df.to_csv('mp_district_schemes_clean.csv', index=False)
print("Clean Dataset Saved! Final Rows:", len(df))