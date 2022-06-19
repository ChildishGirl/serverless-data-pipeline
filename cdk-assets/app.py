from stacks.cicd_stack import *


app = cdk.App()
CICDStack(app, 'CodePipelineStack',
          env=cdk.Environment(account='YOUR_ACCOUNT',
                              region="eu-central-1"))
cdk.Tags.of(app).add('env', 'prod')
cdk.Tags.of(app).add('creator', 'anna-pastushko')
cdk.Tags.of(app).add('owner', 'ml-team')
app.synth()
