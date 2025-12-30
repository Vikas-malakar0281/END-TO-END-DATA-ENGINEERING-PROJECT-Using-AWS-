# 📊 END-TO-END DATA ENGINEERING PROJECT — Using AWS

> This repository contains a complete end-to-end data engineering project built on **AWS Cloud Services**, where we ingest, transform, catalog, query, and analyze YouTube trending data using AWS services.  

---

## 🧠 Project Overview

This project demonstrates how to:

- Ingest large-scale datasets (YouTube Trending stats) into AWS S3.
- Build a **Data Lake** on Amazon S3.
- Catalog and transform raw data into structured formats.
- Query data using **SQL** with AWS Athena.
- Run ETL using AWS Glue and AWS Lambda functions.
- Visualize insights using BI tools (optional).
  
The goal is to turn raw CSV data into analytics-ready parquet tables using serverless AWS services, illustrating a real-world Data Engineering pipeline.

---

## 📁 Dataset Used

We use the **YouTube Trending Video Statistics** dataset from Kaggle:

- Contains daily trending video data (CSV) for multiple regions.
- Includes views, likes, dislikes, category IDs, tags, and other metadata.  
- Regional partitioned folder structure (e.g., `region=us/`, `region=ca/`).

---

## 🧩 Architecture
```
User Local Machine
↓ (Upload AWS cli Commands)
AWS S3 (Raw Bucket)
↓ (Crawler)
AWS Glue Catalog — raw tables
↓ (ETL Jobs / Lambda)
Cleaned S3 (Parquet)
↓ (Glue / Athena)
Athena Views & SQL Analytics
↓ (Visualization)
QuickSight Dashboards
```

---

## 🚀 AWS Services Used

| AWS Service | Purpose |
|-------------|----------|
| **IAM**      | Manage secure access and roles. |
| **S3**       | Raw & transformed data storage (Data Lake). |
| **Glue Crawler** | Scan S3, infer schema and create catalog tables. |
| **AWS Glue Jobs** | ETL using Spark — transform and partition data. |
| **AWS Lambda** | Serverless ETL triggers and conversions. |
| **AWS Athena** | Query data stored in S3 using SQL. |
| **QuickSight** (optional) | BI dashboarding & visualization. | 

---

## 🛠️ Setup & Installation

### 1. 🔐 Create AWS Account & IAM User
  -  Sign up for an AWS account.
  -  Create **IAM Admin user** with programmatic access.
  -  Attach policies: `AmazonS3FullAccess`, `AWSGlueServiceRole`, `AmazonAthenaFullAccess`, etc. 

--- 

### 2. ⚙️ Install AWS CLI

```bash
# macOS / Linux (example)
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
aws configure
Enter AWS Access Key ID, Secret Key, region, and output format. 
```
---

### 3. 📤 Upload Data to S3

- Create an S3 bucket (my-data-lake-bucket).
- Upload the dataset locally to S3 (s3://my-data-lake-bucket/raw/youtube).
- Use aws s3 cp or AWS Console to upload

---

### 🔍 Data Catalog & Crawler

1. In AWS Glue → Crawlers, create a crawler:

    - Data source: s3://my-data-lake-bucket/raw/youtube
    - IAM role with Glue permissions
    - Output database: `youtube_raw_db`
2. Run crawler to auto-create the table schema. 

---

### ✨ ETL — Transform & Clean Data

You can transform data using:

  🧪 Glue Studio / Jobs:
    -   Create a Glue Spark job to transform raw CSV to Parquet.
    -   Partition by fields such as region, category.
    -   Store cleaned outputs in:
        `s3://my-data-lake-bucket/clean/youtube/`

---

### 🌀 Lambda Function (optional)

Use AWS Lambda triggered by S3 events to process new files:
```python
import awswrangler as wr
def lambda_handler(event, context):
    # Read S3 CSV file
    df = wr.s3.read_csv(path="s3://bucket/raw/...")
    # Write to Parquet
    wr.s3.to_parquet(df=df, path="s3://bucket/clean/...", dataset=True)
```
---

### 🧪 Querying with Athena

-  Open AWS Athena.
-  Choose database: youtube_clean_db.
-  Run SQL queries like:

```sql
SELECT region, COUNT(*) AS video_count
FROM youtube_clean
GROUP BY region;
```
Because data is Parquet and partitioned, queries are fast and cost-efficient. 
YouTube

---

### 📊 Visualization

Connect Amazon QuickSight to Athena:
- Create a QuickSight dataset from Athena results.
- Build charts showing views, likes, region trends, etc.

---

### 🔐 Best Practices

Use IAM least privilege — minimal access.

Enable S3 versioning & encryption.

Partition your data efficiently (e.g., by region, date).

Automate with Terraform or CloudFormation.
---
|  📁 Folder Structure  
|  📦 END-TO-END-DATA-ENGINEERING-PROJECT-Using-AWS  
|   ┣ 📂 scripts  
|   ┃ ┣ s3_cli_commands.sh  
|   ┃ ┣ glue_etl_job.py  
|   ┣ 📂 lambda  
|   ┃ ┗ lambda_function.py  
|   ┣ README.md  

---
### 📌 Learnings & Takeaways

✔ Build a scalable AWS Data Lake + ETL pipeline.  
✔ Use Glue Catalog + Athena for SQL analytics on cloud.  
✔ Process and convert CSV → Parquet for performance.  
✔ Understand Glue Crawler, Jobs, Lambda triggers, and permissions.   

---

Happy Coding & Data Engineering! 🚀
