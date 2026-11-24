# Data Dictionary

Table: `mp_district_schemes`

| Column | Type | Description |
|---|---|---|
| Record_ID | Text/Number | Unique record identifier |
| Report_Date | Date | Reporting date |
| District | Text | Madhya Pradesh district name |
| Block | Text | Block within the district |
| Scheme_Name | Text | Welfare scheme (MGNREGA, PM Awas Yojana (Gramin), Ladli Behna Yojana, MP Post-Matric Scholarship, etc.) |
| Applications_Received | Number | Total applications received |
| Approved_Count | Number | Applications approved |
| Rejected_Count | Number | Applications rejected |
| Pending_Count | Number | Applications still pending |
| Approval_Rate_Pct | Decimal | Approval rate in percent |
| Avg_Pending_Days | Decimal | Average number of days cases stay pending |
| Bottleneck_Reason | Text | Main reason for pending cases (e-KYC Incomplete, Document Mismatch, Portal Sync Issue, Bank-Aadhaar Seeding Pending, Field Verification Delay, Under Verification) |
| Fund_Allocated | Number | Fund allocated |
| Fund_Utilized | Number | Fund utilized |
| Fund_Utilization_Pct | Decimal | Fund utilization in percent |

> Verify column names and types against your actual dataset and edit this file if any differ.
