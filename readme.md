# Anonymizer

## Description
This project aims to anonymize documents using Azure services. Anonymization is the process of removing or obscuring personally identifiable information (PII) from documents to protect individuals' privacy.

## Features
- **Text Anonymization**: Removal of personal information from text documents.
- **Multiple Format Support**: Support for documents in formats such as PDF, DOCX, TXT, etc.
- **Azure Integration**: Use of Azure AI Services for PII detection and anonymization.
- **User Interface**: User-friendly interface for document upload and processing.

## Prerequisites
- Azure Account
- Python >= 3.9

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/gilbertossoares/anonimizer.git
    ```
2. Navigate to the project directory:
    ```bash
    cd anonimizer
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements
    ```

## Configuration
1. Create a `.env` file in the project root and add your Azure credentials:
    ```plaintext
    AZURE_STORAGE_CONNECTION_STRING=
    INPUT_CONTAINER_NAME=
    OUTPUT_CONTAINER_NAME=
    AZURE_AI_SEARCH_ENDPOINT=
    AZURE_AI_SEARCH_KEY=
    AZURE_COMPUTER_VISION_ENDPOINT=
    AZURE_COMPUTER_VISION_KEY=
    AZURE_CUSTOM_COMPUTE_VISION_ENDPOINT=
    AZURE_CUSTOM_COMPUTE_VISION_PREDICTION_KEY=
    AZURE_DATALAKE_ACCOUNT_NAME=
    AZURE_FORM_RECOGNIZER_ENDPOINT=
    AZURE_FORM_RECOGNIZER_KEY=
    AZURE_TEXT_ANALYTCIS_ENDPOINT=
    AZURE_TEXT_ANALYTICS_KEY=
    ```

## Usage
1. Start the server:
    ```bash
    python app.py          
    ```
2. Access the user interface in your browser:
    ```plaintext
    http://localhost:5000
    ```
3. Upload a document and start the anonymization process.

## Architecture
This project uses the following architecture:

![Project Architecture](static/images/archteture.png)

## Workflow
The following workflow is the step-by-step path of the file through the solution.

![Workflow](static/images/workflow.png)

## License
This project is licensed under the [MIT License](LICENSE).

---

# Anonimizer

## Descrição
Este projeto tem como objetivo a anonimização de documentos utilizando os serviços da Azure. A anonimização é o processo de remover ou obscurecer informações pessoais identificáveis (PII) de documentos para proteger a privacidade dos indivíduos.

## Funcionalidades
- **Anonimização de Texto**: Remoção de informações pessoais de documentos de texto.
- **Suporte a Múltiplos Formatos**: Suporte para documentos em formatos como PDF, DOCX, TXT, etc.
- **Integração com Azure**: Utilização de serviços Azure AI Services para detecção e anonimização de PII.
- **Interface de Usuário**: Interface amigável para upload e processamento de documentos.

## Pré-requisitos
- Conta na Azure
- Python >= 3.9

## Instalação
1. Clone o repositório:
    ```bash
    git clone https://github.com/gilbertossoares/anonimizer.git
    ```
2. Navegue até o diretório do projeto:
    ```bash
    cd anonimizer
    ```
3. Instale as dependências:
    ```bash
    pip install -r requirements
    ```

## Configuração
1. Crie um arquivo `.env` na raiz do projeto e adicione suas credenciais da Azure:
    ```plaintext
    AZURE_STORAGE_CONNECTION_STRING=
    INPUT_CONTAINER_NAME=
    OUTPUT_CONTAINER_NAME=
    AZURE_AI_SEARCH_ENDPOINT=
    AZURE_AI_SEARCH_KEY=
    AZURE_COMPUTER_VISION_ENDPOINT=
    AZURE_COMPUTER_VISION_KEY=
    AZURE_CUSTOM_COMPUTE_VISION_ENDPOINT=
    AZURE_CUSTOM_COMPUTE_VISION_PREDICTION_KEY=
    AZURE_DATALAKE_ACCOUNT_NAME=
    AZURE_FORM_RECOGNIZER_ENDPOINT=
    AZURE_FORM_RECOGNIZER_KEY=
    AZURE_TEXT_ANALYTCIS_ENDPOINT=
    AZURE_TEXT_ANALYTICS_KEY=
    ```

## Uso
1. Inicie o servidor:
    ```bash
    python app.py          
    ```
2. Acesse a interface de usuário em seu navegador:
    ```plaintext
    http://localhost:5000
    ```
3. Faça upload de um documento e inicie o processo de anonimização.

## Arquitetura
Este projeto utiliza da seguinte arquitetura:

![Arquitetura do Projeto](static/images/archteture.png)

## Workflow
O fluxo de trabalho a seguir é o passo a passo pelo caminho do arquivo através da solução.

![Workflow](static/images/workflow.png)

## Licença
Este projeto está licenciado sob a [MIT License](LICENSE).
