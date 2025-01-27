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
- Python => 3.9

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
    AZURE_COGNITIVE_SERVICES_KEY=your_key_here
    AZURE_COGNITIVE_SERVICES_ENDPOINT=your_endpoint_here
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

## Licença
Este projeto está licenciado sob a [MIT License](LICENSE).
