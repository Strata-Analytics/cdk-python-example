from constructs import Construct
import aws_cdk as cdk


class TransformationStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        source_bucket = cdk.aws_s3.Bucket(
            self,
            "SourceBucket",
            bucket_name="demo-strata-source",
            removal_policy=cdk.RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        target_bucket = cdk.aws_s3.Bucket(
            self,
            "TargetBucket",
            bucket_name="demo-strata-target",
            removal_policy=cdk.RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        layer = cdk.aws_lambda.LayerVersion.from_layer_version_arn(
            self,
            "AWSWranglerLayer",
            "arn:aws:lambda:us-east-1:336392948345:layer:AWSSDKPandas-Python312:12",
        )

        lambda_function = cdk.aws_lambda.Function(
            self,
            "LambdaFunction",
            function_name="convert-csv-parquet",
            runtime=cdk.aws_lambda.Runtime.PYTHON_3_12,
            code=cdk.aws_lambda.Code.from_asset("lambda/convert-csv-parquet"),
            handler="index.handler",
            layers=[layer],
            retry_attempts=0,
            memory_size=256,
            timeout=cdk.Duration.seconds(10),
            environment={
                "SOURCE_BUCKET": source_bucket.bucket_name,
                "TARGET_BUCKET": target_bucket.bucket_name,
            },
        )

        source_bucket.add_event_notification(
            cdk.aws_s3.EventType.OBJECT_CREATED,
            cdk.aws_s3_notifications.LambdaDestination(lambda_function),
        )

        source_bucket.grant_read(lambda_function)
        target_bucket.grant_write(lambda_function)
