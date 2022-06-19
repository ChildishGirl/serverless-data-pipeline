import aws_cdk as cdk
import aws_cdk.aws_iam as _iam
import aws_cdk.aws_chatbot as _chatbot
import aws_cdk.aws_codecommit as _ccommit
from stacks.data_pipeline_stage import *
import aws_cdk.aws_codestarnotifications as _notifications
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep


class CICDStack(cdk.Stack):

    def __init__(self, scope, construct_id, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # Create reference to CodeCommit repository
        pipeline_repo = _ccommit.Repository.from_repository_name(self, 'data_pipeline_repository',
                                                                 repository_name='data_pipeline_repository')

        # Create CodePipeline and add stage to deploy data pipeline
        cicd_pipeline = CodePipeline(self, 'cicd_pipeline',
                                     pipeline_name='cicd_pipeline',
                                     docker_enabled_for_synth=True,
                                     self_mutation=True,
                                     synth=ShellStep('Synth',
                                                     input=CodePipelineSource.code_commit(pipeline_repo, 'main'),
                                                     commands=['npm install -g aws-cdk',
                                                               'python -m pip install -r requirements.txt',
                                                               'cdk synth']))
        cicd_pipeline.add_stage(DataPipelineStage(self, 'DataPipelineDeploy'))
        cicd_pipeline.build_pipeline()

        # Add Slack notifications
        slack = _chatbot.SlackChannelConfiguration(self, 'MySlackChannel',
                                                   slack_channel_configuration_name='announcements',
                                                   slack_workspace_id='YOUR_ID',
                                                   slack_channel_id='YOUR_ID')
        slack.role.attach_inline_policy(_iam.Policy(self, 'slack_policy',
                                                    statements=[_iam.PolicyStatement(effect=_iam.Effect.ALLOW,
                                                                                     actions=['chatbot:*'],
                                                                                     resources=['*'])]))

        _notifications.NotificationRule(self, 'NotificationRule',
                                        source=cicd_pipeline.pipeline,
                                        detail_type=_notifications.DetailType.FULL,
                                        events=['codepipeline-pipeline-pipeline-execution-started',
                                                'codepipeline-pipeline-pipeline-execution-succeeded',
                                                'codepipeline-pipeline-pipeline-execution-failed'],
                                        targets=[slack])
