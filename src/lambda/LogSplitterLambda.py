# FUNÇÃO DE TESTE LOCAL

# import os
# import boto3
# from pathlib import Path
# from dotenv import load_dotenv

# load_dotenv()

# caminho = Path("/Users/tarcisiocouto/VSCode Projects/desafio-aws-logbatchprocessor/logs/application.txt")

# AWS_SQS_QUEUE_URL = os.getenv('AWS_SQS_QUEUE_URL')
# print(AWS_SQS_QUEUE_URL)

# aws_client = boto3.client('sqs')

# count = 0
# with open(caminho, 'r') as file:
#     for line in file:
#         aws_client.send_message(
#             QueueUrl=AWS_SQS_QUEUE_URL,
#             MessageBody=line
#         )
#         count = count + 1
#         print(f'Message sent to SQS - {count}: {line}')

# FUNÇÃO LAMBDA AWS

import os
import json
import boto3

AWS_SQS_QUEUE_URL = os.getenv('AWS_SQS_QUEUE_URL')

def lambda_handler(event, context):
    aws_client_sqs = boto3.client('sqs')
    aws_client_s3 = boto3.client('s3')
    key = event['Records'][0]['s3']['object']['key']
    bucket = event['Records'][0]['s3']['bucket']['name']

    response = aws_client_s3.get_object(Bucket=bucket, Key=key)
    content = response['Body'].read().decode('utf-8')

    for line in content.splitlines():
        aws_client_sqs.send_message(QueueUrl=AWS_SQS_QUEUE_URL, MessageBody=line)
  
    return {
        'statusCode': 200,
        'body': 'Logs were send to SQSS'
    }