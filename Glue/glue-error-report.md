# 📄 AWS Glue ETL Error Report & Resolutions

Project: End-to-End YouTube Data Engineering (AWS Glue + Spark)  
Author: Vikas Malakar  
Glue Version: 5.0 (Spark 3.5, Python 3)  
Data Source: Multi-region YouTube CSV dataset  

## 📌 Overview

While building an AWS Glue Visual ETL job to convert multi-region YouTube CSV files into a single analytics-ready Parquet dataset, several real-world production errors were encountered.

This document explains:

  -  What each error means

  -  Why it occurred

  -  The exact solution applied

These issues are common in enterprise-scale ETL pipelines and the solutions reflect industry best practices.

## ❌ Error 1: Athena / Glue Schema Confusion for IDs
### 🔴 Error / Issue

- video_id values like:

```nginx
v4uraQbxIUg
```

- Caused query and schema confusion

### 💡 Root Cause

`video_id` is **alphanumeric**

Incorrectly assumed to be numeric

### ✅ Solution

Defined `video_id` as **STRING** in Glue schema and ApplyMapping
```python
("video_id", "string", "video_id", "string")
```

## ❌ Error 2: `region` Column Not Created Automatically
### 🔴 Error

- Glue did not create `region` column from:

```bash
s3://bucket/raw-data/region=ca/file.csv
```

### 💡 Root Cause

- Glue Studio S3 Source does not auto-extract partitions

- Folder names are treated as plain directories

### ✅ Solution

- Extracted `region` manually using Spark:

```python
df = df.withColumn(
    "region",
    regexp_extract(input_file_name(), "region=([^/]+)", 1)
)
```

## ❌ Error 3: Unable to Parse `MXvideos.csv`
### 🔴 Error Message

```
Error Category: UNCLASSIFIED_ERROR; Failed Line Number: 24; An error occurred while calling o158.toDF. Unable to parse file: MXvideos.csv
```

### 💡 Root Cause

- Multiline descriptions

- Unescaped quotes

- Malformed UTF-8 characters

### ✅ Solution

- Used Spark CSV reader with PERMISSIVE mode and multiline support

```python
spark.read \
  .option("multiLine", "true") \
  .option("mode", "PERMISSIVE")
```

## ❌ Error 4: `.toDF()` Failure on DynamicFrame
### 🔴 Error

```
 DynamicFrame → DataFrame conversion failed
```

### 💡 Root Cause

- DynamicFrame is tolerant

- DataFrame is strict with malformed CSV

### ✅ Solution

- Read CSV directly using Spark

- Convert to DynamicFrame only after cleaning

## ❌ Error 5: `LongType vs stringnode` (Numeric Columns)
### 🔴 Error Message
```
Unsupported case of DataType: LongType and DynamicNode: stringnode
```

### 💡 Root Cause

- Spark reads all CSV columns as STRING

- Glue ApplyMapping expected numeric types

### ✅ Solution

- Explicitly cast numeric columns in Spark
```python
df = df.withColumn("views", col("views").cast("long"))
```

## ❌ Error 6: BooleanType vs stringnode
### 🔴 Error Message

```
Unsupported case of DataType: BooleanType and DynamicNode: stringnode
```

### 💡 Root Cause

- Boolean fields stored as "true" / "false" strings

- Glue does not auto-cast booleans

### ✅ Solution

- Normalized and cast boolean fields explicitly

```python
df = df.withColumn(
    "comments_disabled",
    when(lower(col("comments_disabled")) == "true", True)
    .otherwise(False)
)
```

## ❌ Error 7: Timestamp Conversion Failure
### 🔴 Error

Failed cast from string → timestamp

### 💡 Root Cause

```
ISO-8601 timestamp format in CSV
```

### ✅ Solution

- Used to_timestamp with explicit format

```python
to_timestamp("publish_time", "yyyy-MM-dd'T'HH:mm:ss.SSS'Z'")
```

## ❌ Error 8: Missing Import (col not defined)
### 🔴 Error Message
```
Error Category: INVALID_ARGUMENT_ERROR; Failed Line Number: 48; NameError: name 'col' is not defined
```

### 💡 Root Cause

- Forgot to import col from Spark functions

### ✅ Solution
```python
from pyspark.sql.functions import col
```

### ✅ Final Outcome

✔ Successfully processed malformed multilingual CSV data
✔ Converted data into Snappy-compressed Parquet
✔ Partitioned by region
✔ Glue Data Catalog updated automatically
✔ Athena queries work without errors


