# Use AWS cloud provider

* Status: accepted
* Date: 2022-05-12

## Context and Problem Statement

We want to develop serverless data pipeline which will be running in the cloud.
Which cloud provider shoukd be used?

## Considered Options

* Amazon Web Services
* Google Cloud Platform
* Microsoft Azure

## Decision Outcome

Chosen option: Amazon Web Services, because

* Data science team uses SageMaker as development environment.
* All other data workloads are in AWS cloud.
