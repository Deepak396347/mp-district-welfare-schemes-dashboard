import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)

# 5 Key Districts (including Vacant Districts) & their Real Blocks
district_blocks = {
    'Indore': ['Indore Urban', 'Mhow', 'Depalpur', 'Sanwer'],
    'Singrauli': ['Waidhan', 'Deosar', 'Chitrangi'],
    'Jabalpur': ['Jabalpur', 'Kundam', 'Patan', 'Sihora', 'Majholi'],
    'Ujjain': ['Ujjain', 'Nagda', 'Mahidpur', 'Tarana', 'Badnagar'],
    'Gwalior': ['Gwalior (Morar)', 'Dabra', 'Bhitarwar', 'Ghatigaon']
}

schemes = [
    'Ladli Behna Yojana',
    'PM Awas Yojana (Gramin)',
    'MGNREGA',
    'MP Post-Matric Scholarship'
]

bottlenecks = [
    'Bank-Aadhaar Seeding Pending',
    'e-KYC Incomplete',
    'Field Verification Delay',
    'Document Mismatch',
    'Portal Sync Issue'
]

rows = []
base_date = datetime(2026, 4, 1)

# Generating 10,000 clean-structure rows with realistic regional disparities
for i in range(1, 10001):
    dist = random.choice(list(district_blocks.keys()))
    block = random.choice(district_blocks[dist])
    scheme = random.choice(schemes)
    report_date = base_date + timedelta(days=random.randint(0, 210))
    
    apps_received = random.randint(80, 450)
    
    # Realistic lag in specific blocks (Chitrangi & Kundam)
    if block in ['Chitrangi', 'Kundam']:
        approval_rate = random.uniform(0.50, 0.65)
    elif dist in ['Indore', 'Ujjain']:
        approval_rate = random.uniform(0.80, 0.92)
    else:
        approval_rate = random.uniform(0.68, 0.82)
        
    approved = int(apps_received * approval_rate)
    rejected = int((apps_received - approved) * random.uniform(0.15, 0.30))
    pending = apps_received - approved - rejected
    
    fund_allocated = round(apps_received * random.uniform(0.12, 0.35), 2) # in Lakhs
    fund_utilized = round(fund_allocated * (approved / apps_received) * random.uniform(0.90, 1.0), 2)
    
    pending_days = random.randint(25, 65) if block in ['Chitrangi', 'Kundam'] else random.randint(5, 28)
    reason = random.choice(bottlenecks) if pending > 0 else 'None'
    
    rows.append([
        f"REC-{10000+i}", dist, block, scheme, report_date.strftime('%Y-%m-%d'),
        apps_received, approved, pending, rejected,
        fund_allocated, fund_utilized, pending_days, reason
    ])

columns = [
    'Record_ID', 'District', 'Block', 'Scheme_Name', 'Report_Date',
    'Applications_Received', 'Approved_Count', 'Pending_Count', 'Rejected_Count',
    'Fund_Allocated_Lakhs', 'Fund_Utilized_Lakhs', 'Avg_Pending_Days', 'Bottleneck_Reason'
]

df = pd.DataFrame(rows, columns=columns)

# --- INTENTIONALLY ADDING DIRTY DATA FOR STEP 3 (DATA CLEANING) ---
# 1. Missing values (~300 rows)
for idx in np.random.choice(df.index, 180, replace=False):
    df.loc[idx, 'Bottleneck_Reason'] = np.nan
for idx in np.random.choice(df.index, 120, replace=False):
    df.loc[idx, 'Fund_Utilized_Lakhs'] = np.nan

# 2. Incorrect / Logical Errors (~80 rows where Approved > Received)
for idx in np.random.choice(df.index, 80, replace=False):
    df.loc[idx, 'Approved_Count'] = df.loc[idx, 'Applications_Received'] + random.randint(10, 40)

# 3. Duplicate records (250 duplicate rows -> Total = 10,250 rows)
duplicates = df.sample(250, random_state=42)
df_dirty = pd.concat([df, duplicates], ignore_index=True)

df_dirty.to_csv('mp_district_schemes_raw.csv', index=False)
print(f"Dataset generated! Total Rows: {len(df_dirty)}")