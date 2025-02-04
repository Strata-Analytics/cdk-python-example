import os
import awswrangler as wr


def handler(event, _):
    source_bucket = os.getenv("SOURCE_BUCKET")
    target_bucket = os.getenv("TARGET_BUCKET")

    source_key = event["Records"][0]["s3"]["object"]["key"]
    target_key = source_key.replace(".csv", ".parquet")

    csv_file_path = f"s3://{source_bucket}/{source_key}"
    parquet_file_path = f"s3://{target_bucket}/{target_key}"

    df = wr.s3.read_csv(csv_file_path)

    wr.s3.to_parquet(df=df, path=parquet_file_path, compression="snappy")

    print(f"Converted {source_key} to Parquet and saved as {target_key}")

    return {
        "statusCode": 200,
        "body": f"Converted {source_key} to Parquet and saved as {target_key}",
    }
