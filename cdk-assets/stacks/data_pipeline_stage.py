import aws_cdk as cdk
from constructs import Construct
from stacks.data_pipeline_stack import *

class DataPipelineStage(cdk.Stage):
    def __init__(self, scope, construct_id, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        DataPipelineStack(self, 'DataPipelineStack')
