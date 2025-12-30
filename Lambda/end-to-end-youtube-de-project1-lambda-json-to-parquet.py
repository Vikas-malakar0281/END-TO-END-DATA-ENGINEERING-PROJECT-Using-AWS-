import awswrangler as wr
import pandas as pd
import urllib.parse
import boto3
import os

def lambda_handler(event, context):

    glue = boto3.client("glue")

    s3_base_path = os.environ["cleaned_s3_layer"]
    db_name = os.environ["glue_catelog_db_name"]
    table_name = os.environ["glue_catelog_table_name"]

    # ✅ Ensure Glue DB exists
    try:
        glue.get_database(Name=db_name)
    except glue.exceptions.EntityNotFoundException:
        glue.create_database(DatabaseInput={"Name": db_name})

    # Get S3 event details
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(
        event['Records'][0]['s3']['object']['key'],
        encoding='utf-8'
    )

    try:
        df_raw = wr.s3.read_json(f"s3://{bucket}/{key}")
        df_step_1 = pd.json_normalize(df_raw["items"])

        # ✅ Proper dataset path
        dataset_path = f"{s3_base_path}/"

        return wr.s3.to_parquet(
            df=df_step_1,
            path=dataset_path,
            dataset=True,
            database=db_name,
            table=table_name,
            mode="append"
        )

    except Exception as e:
        print(e)
        print(f"Error processing object {key} from bucket {bucket}")
        raise e
