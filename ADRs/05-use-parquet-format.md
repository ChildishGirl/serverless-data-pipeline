
# Use Parquet format

* Status: accepted
* Date: 2022-05-12

## Context and Problem Statement

We want to store processed data in efficient maner.
Which format should we use?

## Considered Options

* Matlab
* Parquet/Avro/Arrow
* CSV

## Decision Outcome

Chosen option: Parquet, because

* Parquet files is the most efficient option for quering via Athena.
* Parquet files more cost effective option compared with .csv.
* Parquet can be asily parsed using Python by data science team.
