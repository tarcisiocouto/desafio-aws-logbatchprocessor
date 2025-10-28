import os
import boto3
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

AWS_S3_INPUT_LOG = os.getenv('AWS_S3_INPUT_LOG')

caminho = Path("/Users/tarcisiocouto/VSCode Projects/desafio-aws-logbatchprocessor/logs/logs.txt")

def send_file_to_s3():
    aws_client = boto3.client('s3')    
    aws_client.upload_file(
        Filename=caminho,
        Bucket=AWS_S3_INPUT_LOG,
        Key=caminho.name,
        )
    print(f'File uploaded to S3: {caminho.name}')


