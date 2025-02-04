#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_python_example.cdk_python_example_stack import TransformationStack


app = cdk.App()
TransformationStack(app, "TransformationStack")

app.synth()
