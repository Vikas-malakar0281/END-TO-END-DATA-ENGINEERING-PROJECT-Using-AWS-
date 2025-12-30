import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import (
    to_timestamp,
    input_file_name,
    regexp_extract,
    col
)
from awsglue.dynamicframe import DynamicFrame

# -----------------------------------
# Job setup
# -----------------------------------
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# -----------------------------------
# Read CSV safely (handles MX, RU, KR files)
# -----------------------------------
df = spark.read \
    .option("header", "true") \
    .option("multiLine", "true") \
    .option("quote", "\"") \
    .option("escape", "\"") \
    .option("mode", "PERMISSIVE") \
    .option("encoding", "UTF-8") \
    .csv("s3://end-to-end-youtube-de-project1/youtube/raw-statics-data/")

# -----------------------------------
# Extract region from S3 folder name
# -----------------------------------
df = df.withColumn(
    "region",
    regexp_extract(input_file_name(), "region=([^/]+)", 1)
)

# -----------------------------------
# Cast numeric columns 
# -----------------------------------
df = df \
    .withColumn("category_id", col("category_id").cast("long")) \
    .withColumn("views", col("views").cast("long")) \
    .withColumn("likes", col("likes").cast("long")) \
    .withColumn("dislikes", col("dislikes").cast("long")) \
    .withColumn("comment_count", col("comment_count").cast("long"))

# -----------------------------------
# Safe timestamp conversion
# -----------------------------------
df = df.withColumn(
    "publish_time",
    to_timestamp("publish_time", "yyyy-MM-dd'T'HH:mm:ss.SSS'Z'")
)

# -----------------------------------
# Convert to DynamicFrame for Glue transforms
# -----------------------------------
source_dyf = DynamicFrame.fromDF(df, glueContext, "source_dyf")

# -----------------------------------
# Apply schema mapping
# -----------------------------------
mapped_dyf = ApplyMapping.apply(
    frame=source_dyf,
    mappings=[
        ("video_id", "string", "video_id", "string"),
        ("trending_date", "string", "trending_date", "string"),
        ("title", "string", "title", "string"),
        ("channel_title", "string", "channel_title", "string"),
        ("category_id", "long", "category_id", "bigint"),
        ("publish_time", "timestamp", "publish_time", "timestamp"),
        ("tags", "string", "tags", "string"),
        ("views", "long", "views", "bigint"),
        ("likes", "long", "likes", "bigint"),
        ("dislikes", "long", "dislikes", "bigint"),
        ("comment_count", "long", "comment_count", "bigint"),
        ("thumbnail_link", "string", "thumbnail_link", "string"),
        ("comments_disabled", "boolean", "comments_disabled", "boolean"),
        ("ratings_disabled", "boolean", "ratings_disabled", "boolean"),
        ("video_error_or_removed", "boolean", "video_error_or_removed", "boolean"),
        ("description", "string", "description", "string"),
        ("region", "string", "region", "string")
    ]
)

# -----------------------------------
# Write Parquet + update Glue Catalog
# -----------------------------------
sink = glueContext.getSink(
    path="s3://end-to-end-youtube-de-project1-cleaned/youtube/clean-statistic-data/",
    connection_type="s3",
    updateBehavior="UPDATE_IN_DATABASE",
    partitionKeys=["region"],
    enableUpdateCatalog=True
)

sink.setCatalogInfo(
    catalogDatabase="de-youtube-project-clean-db",
    catalogTableName="clean_statics_data"
)

sink.setFormat("glueparquet", compression="snappy")
sink.writeFrame(mapped_dyf)

job.commit()
