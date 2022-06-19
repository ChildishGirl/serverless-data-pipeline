
# Use SQS service

* Status: accepted
* Date: 2022-05-12

## Context and Problem Statement

We want to trigger Lambda by S3 file upload event.
How should we pass these events?

## Considered Options

* S3 -> SQS -> Lambda
* S3 -> Lambda

## Decision Outcome

Chosen option: S3 -> SQS -> Lambda, because

* If the Lambda function does not return success, the message will not be deleted from the queue.
* If number of events exceeds Lambda concurency limit, events will not be lost.
