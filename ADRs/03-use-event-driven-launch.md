
# Use event-driven launch for pipeline

* Status: accepted
* Date: 2022-05-12

## Context and Problem Statement

We want to launch pipeline execution. How should we do it?

## Considered Options

* Event-driven launch
* Schedled launch
* Manual launch

## Decision Outcome

Chosen option: event-driven launch, because

* Data should be processed as soon as it is uploaded.
* It is not possible to predict when data will be available.
* For manual launch we need dedicated person to monitor data upload.
