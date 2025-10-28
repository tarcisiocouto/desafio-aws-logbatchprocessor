
# Desafio AWS Log Batch Processor

Este projeto demonstra o processamento de logs em lote utilizando serviços da AWS. Ele é composto por dois scripts principais: um para enviar arquivos de log para o S3 e uma função Lambda para processar esses arquivos.

## Arquitetura

A arquitetura deste projeto é baseada em eventos e utiliza os seguintes serviços da AWS:

- **Amazon S3 (Simple Storage Service):** Utilizado como repositório para armazenar os arquivos de log. O script `send_file_to_s3.py` é responsável por enviar os arquivos para um bucket de entrada.

- **AWS Lambda:** Uma função Lambda (`LogSplitterLambda.py`) é acionada sempre que um novo arquivo de log é adicionado ao bucket S3. A função lê o arquivo, divide-o em linhas e envia cada linha como uma mensagem para uma fila SQS.

- **Amazon SQS (Simple Queue Service):** Uma fila SQS é utilizada para armazenar as mensagens de log enviadas pela função Lambda. Essas mensagens podem ser posteriormente processadas por outros serviços ou aplicações.

## Scripts

### `src/send_file_to_s3.py`

Este script é responsável por enviar um arquivo de log local para um bucket S3. Ele utiliza a biblioteca `boto3` para interagir com a AWS.

**Linha a linha:**

- **`import os`:** Módulo para interagir com o sistema operacional, usado para obter variáveis de ambiente.
- **`import boto3`:** A biblioteca da AWS para Python, que permite criar, configurar e gerenciar serviços da AWS.
- **`from dotenv import load_dotenv`:** Função para carregar variáveis de ambiente de um arquivo `.env`.
- **`from pathlib import Path`:** Módulo para manipulação de caminhos de arquivos de forma orientada a objetos.
- **`load_dotenv()`:** Carrega as variáveis de ambiente do arquivo `.env` para o ambiente de execução.
- **`AWS_S3_INPUT_LOG = os.getenv('AWS_S3_INPUT_LOG')`:** Obtém o nome do bucket S3 de entrada da variável de ambiente `AWS_S3_INPUT_LOG`.
- **`caminho = Path(...)`:** Define o caminho do arquivo de log local a ser enviado.
- **`def send_file_to_s3():`:** Define a função principal que realiza o upload do arquivo.
- **`aws_client = boto3.client('s3')`:** Cria um cliente S3 do `boto3`, que permite interagir com o serviço S3.
- **`aws_client.upload_file(...)`:** Realiza o upload do arquivo para o S3 com os seguintes parâmetros:
    - **`Filename`:** O caminho do arquivo local.
    - **`Bucket`:** O nome do bucket S3 de destino.
    - **`Key`:** O nome do objeto no S3 (neste caso, o nome do arquivo).
- **`print(...)`:** Exibe uma mensagem de confirmação após o upload.

### `src/lambda/LogSplitterLambda.py`

Esta função Lambda é acionada por um evento S3. Ela lê o arquivo de log, divide-o em linhas e envia cada linha para uma fila SQS.

**Linha a linha:**

- **`import os`:** Módulo para obter variáveis de ambiente.
- **`import json`:** Módulo para manipulação de JSON (não utilizado diretamente no código principal, mas comum em funções Lambda).
- **`import boto3`:** A biblioteca da AWS para Python.
- **`AWS_SQS_QUEUE_URL = os.getenv('AWS_SQS_QUEUE_URL')`:** Obtém a URL da fila SQS da variável de ambiente `AWS_SQS_QUEUE_URL`.
- **`def lambda_handler(event, context):`:** A função principal da Lambda, que recebe o evento (neste caso, do S3) e o contexto de execução.
- **`aws_client_sqs = boto3.client('sqs')`:** Cria um cliente SQS do `boto3`.
- **`aws_client_s3 = boto3.client('s3')`:** Cria um cliente S3 do `boto3`.
- **`key = event['Records'][0]['s3']['object']['key']`:** Extrai a chave (nome do arquivo) do objeto S3 do evento.
- **`bucket = event['Records'][0]['s3']['bucket']['name']`:** Extrai o nome do bucket S3 do evento.
- **`response = aws_client_s3.get_object(Bucket=bucket, Key=key)`:** Obtém o objeto do S3 usando o nome do bucket e a chave.
- **`content = response['Body'].read().decode('utf-8')`:** Lê o corpo do objeto e decodifica para uma string UTF-8.
- **`for line in content.splitlines():`:** Itera sobre cada linha do conteúdo do arquivo.
- **`aws_client_sqs.send_message(...)`:** Envia cada linha como uma mensagem para a fila SQS especificada.
- **`return { ... }`:** Retorna uma resposta HTTP de sucesso.

## Conceitos da AWS

- **S3 Bucket:** Um "balde" (bucket) no S3 é um contêiner para objetos (arquivos). Cada bucket tem um nome único globalmente.

- **S3 Object:** Um objeto no S3 é um arquivo e seus metadados. Cada objeto é identificado por uma chave (key) única dentro de um bucket.

- **S3 Key:** A chave (key) de um objeto S3 é o seu identificador único dentro de um bucket. É análoga ao nome de um arquivo em um sistema de arquivos.

- **`get_object`:** A operação `get_object` do `boto3` permite recuperar um objeto de um bucket S3. Você precisa fornecer o nome do bucket e a chave do objeto para obter seu conteúdo.

## Como executar

1.  **Configure as variáveis de ambiente:** Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

    ```
    AWS_S3_INPUT_LOG=seu-bucket-de-entrada
    AWS_SQS_QUEUE_URL=sua-url-da-fila-sqs
    ```

2.  **Execute o script de upload:**

    ```bash
    python src/send_file_to_s3.py
    ```

3.  **Deploy da função Lambda:** Faça o deploy da função `LogSplitterLambda.py` no AWS Lambda e configure um gatilho S3 para o bucket de entrada.
