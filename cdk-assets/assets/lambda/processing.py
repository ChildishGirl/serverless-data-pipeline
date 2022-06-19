import io
import json
import os
import boto3
import urllib3
import logging
import scipy.io
import pandas as pd
import pathlib as pl
import awswrangler as wr
from urllib.parse import unquote_plus


s3 = boto3.client('s3')
sqs = boto3.client('sqs')


def handler(event, context):
    # Parse event and get file name
    message_rh = event['Records'][0]['receiptHandle']
    key = json.loads(event['Records'][0]['body'])['Records'][0]['s3']['object']['key']
    key = unquote_plus(key)
    raw_bucket = json.loads(event['Records'][0]['body'])['Records'][0]['s3']['bucket']['name']
    processed_bucket = 'processed-ecg-data'

    try:
        # Read mat file
        _obj = s3.get_object(Bucket=raw_bucket, Key=key)['Body'].read()
        raw_data = scipy.io.loadmat(io.BytesIO(_obj))

        # Clean data
        _df = pd.DataFrame(raw_data['val'][0], columns=['ECG_data'])
        _df.fillna(method='pad', inplace=True)
        _df['ECG_data'] = (_df['ECG_data'] - _df['ECG_data'].min()) / (_df['ECG_data'].max() - _df['ECG_data'].min())

        # Save parquet file to verified bucket
        file_name = pl.Path(key).stem
        wr.s3.to_parquet(df=_df, path=f's3://{processed_bucket}/{file_name}.parquet')
        logging.info(f'File {file_name} was successfully processed.')

    except Exception:
        # Send notification about failure to Slack channel
        _url = 'https://hooks.slack.com/YOUR_HOOK'
        _msg = {'text': f'Processing of {key} was unsuccessful.'}
        http = urllib3.PoolManager()
        resp = http.request(method='POST', url=_url, body=json.dumps(_msg).encode('utf-8'))
        # Write message to logs
        logging.error(f'Processing of {key} was unsuccessful.', exc_info=True)

    # Delete processed message from SQS
    sqs.delete_message(
        QueueUrl=os.environ.get('QueueUrl'),
        ReceiptHandle=message_rh)
