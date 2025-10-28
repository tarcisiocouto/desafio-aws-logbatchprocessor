Com certeza! O desafio anterior focou na **criação assíncrona**. Para o próximo, vamos focar no **processamento de arquivos em lote** (batch processing), que é um cenário real e excelente para explorar a integração entre S3, SQS e Lambda.

Este desafio se chamará **"Processador de Arquivos de Log em Lote (LogBatchProcessor)"**.

---

# Desafio Backend AWS: Processador de Arquivos de Log em Lote (LogBatchProcessor)

## Visão Geral

O objetivo é construir uma arquitetura que processa arquivos grandes de log ou dados de entrada (CSV, JSONL) armazenados no S3. O processamento deve ser feito linha por linha pelo AWS Lambda, usando o SQS para garantir a resiliência e a capacidade de reprocessamento.

## Arquitetura e Serviços AWS Envolvidos

| Serviço | Função no Projeto | Objetivo de Estudo |
| :--- | :--- | :--- |
| **AWS S3** | **Bucket de Entrada (`input-logs`)** e **Bucket de Saída (`processed-data`)**. | **Gatilhos de Evento**, manipulação de arquivos grandes (streaming) e armazenamento de resultados. |
| **AWS SQS** | Fila de Mensagens (`log-processing-queue`). | Resiliência, **processamento de itens individuais** de um lote. |
| **AWS Lambda (Função 1)** | `LogSplitterLambda`. | Acionada pelo S3. **Lê o arquivo grande, quebra em linhas** e envia cada linha como uma mensagem separada para o SQS. |
| **AWS Lambda (Função 2)** | `LogProcessorWorker`. | Acionada pelo SQS. Processa a linha de log individualmente e armazena o resultado no DynamoDB. |
| **Amazon DynamoDB** | Banco de Dados (`ProcessedLogsTable`). | Persistência dos resultados do processamento em lote. |

---

## Fases do Desafio (Requisitos Funcionais)

### Fase 1: Ingestão de Dados e Divisão (S3 -> Lambda 1 -> SQS)

**Objetivo:** Capturar o upload de um arquivo grande, ler seu conteúdo e quebrar o trabalho em pequenas mensagens SQS.

| Tarefa | Detalhamento de Implementação na AWS | Checklist |
| :--- | :--- | :--- |
| **1.1. Configuração do S3** | Criar o bucket de entrada: `input-logs-<seu-nome>`. | [ ] |
| **1.2. Configuração do SQS** | Criar a fila SQS padrão: `log-processing-queue`. | [ ] |
| **1.3. Criação do AWS Lambda 1 (`LogSplitterLambda`)** | Criar o Lambda (Python). **Configurar o S3 como *trigger***: o Lambda deve ser acionado sempre que um novo arquivo (`.txt` ou `.jsonl`) for adicionado ao bucket `input-logs`. | [ ] |
| **1.4. Lógica de Divisão** | O código Python deve: 1) Receber o nome do arquivo do evento S3. 2) Usar `boto3` para ler o arquivo do S3 **linha por linha** (para evitar o carregamento de arquivos gigantes na memória do Lambda). 3) Para cada linha, enviar uma mensagem individual para a fila `log-processing-queue`. | [ ] |

### Fase 2: Processamento de Item Individual (AWS Lambda 2 + DynamoDB)

**Objetivo:** O worker deve processar cada linha de log (mensagem SQS) e salvar um registro processado no banco de dados.

| Tarefa | Detalhamento de Implementação na AWS | Checklist |
| :--- | :--- | :--- |
| **2.1. Configuração do DynamoDB** | Criar a tabela DynamoDB chamada `ProcessedLogsTable`. Chave primária: `id` (UUID/String). | [ ] |
| **2.2. Criação do AWS Lambda 2 (`LogProcessorWorker`)** | Criar a função Lambda (Python). | [ ] |
| **2.3. Conexão SQS -> Lambda** | Configurar o SQS (`log-processing-queue`) como *trigger* do AWS Lambda 2. **O Lambda 2 deve ter permissão de `dynamodb:PutItem`.** | [ ] |
| **2.4. Lógica de Processamento** | O código Python deve: 1) Receber a linha do log da mensagem SQS. 2) Simular um processamento (ex: extrair um `timestamp` ou um `status_code`). 3) Gerar um UUID para o `id`. 4) Salvar o registro processado (ID, Timestamp, Status, Log Original) no DynamoDB. | [ ] |

### Fase 3: Geração de Relatório Consolidado (S3)

**Objetivo:** Criar um mecanismo para registrar quando o processamento do lote termina e gerar um arquivo de "resumo".

| Tarefa | Detalhamento de Implementação na AWS | Checklist |
| :--- | :--- | :--- |
| **3.1. Configuração do S3 de Saída** | Criar o bucket S3 de saída: `processed-data-<seu-nome>`. | [ ] |
| **3.2. Mecanismo de Contagem** | Adicione um campo na tabela DynamoDB (`ProcessedLogsTable`) que armazene o `batch_id` (o nome do arquivo original do S3). | [ ] |
| **3.3. Simulação de Relatório** | **(No Lambda 1 ou um terceiro Lambda)**: Após processar o arquivo, o sistema deve salvar um pequeno arquivo no S3 de saída (`processed-data`) chamado `relatorio_nome-do-arquivo.json`, contendo métricas simples (ex: "Status: Completo", "Total de Itens Processados: X"). | [ ] |

---

## 4. Desafio de Robustez (Extra Credit)

* **Implementar DLQ (Dead-Letter Queue):** Configurar uma DLQ para a fila SQS. Se o `LogProcessorWorker` falhar em processar uma mensagem (linha de log), essa mensagem deve ir para a DLQ após um número de tentativas.
* **Controle de Lotes:** Faça o *LogProcessorWorker* ser idempotente (capaz de lidar com reenvios do SQS sem duplicar dados no DynamoDB).