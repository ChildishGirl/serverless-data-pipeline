
# Use CDK to deploy resources

* Status: accepted
* Date: 2022-05-12

## Context and Problem Statement

We want to use IaC to deploy our resources.
Which tool should we use?

## Considered Options

* Terraform
* CDK
* CloudFormation

## Decision Outcome

Chosen option: CDK, because

* CDK allows to provision infrastructure using language of your choice.
* CDK simplifies definition of resources by providing default values for oprional arguments.
* Developers can quickly and easily review infrastructure.
* CDK allows to detect drifts.
