# Projeto Serverless Completo com Azure Functions e Cosmos DB

Este projeto demonstra uma solução completa para manipulação de dados e arquivos usando Azure Functions, com persistência em Azure Blob Storage e Azure Cosmos DB.

## ✨ Funcionalidades

O projeto contém um único Function App com quatro endpoints HTTP:

1.  **`POST /api/files/upload`**: Faz upload de um arquivo para um contêiner de blob chamado `uploads`.
2.  **`POST /api/documents`**: Cria um novo documento JSON no Cosmos DB.
3.  **`GET /api/documents`**: Lista todos os documentos existentes no Cosmos DB.
4.  **`GET /api/documents/filter?category={value}`**: Filtra documentos no Cosmos DB pela propriedade `category`.

---

## ☁️ 1. Criando a Infraestrutura na Azure

Execute os comandos abaixo no seu terminal (usando Azure CLI) para criar todos os recursos necessários.

```bash
# --- Variáveis (personalize se desejar) ---
RESOURCE_GROUP="rg-serverless-project"
LOCATION="brazilsouth"
STORAGE_ACCOUNT="stserverlessproject$RANDOM"
COSMOSDB_ACCOUNT="cosmos-serverless-project-$RANDOM"
FUNCTION_APP_NAME="func-serverless-project-$RANDOM"

# --- Criação dos Recursos ---

# 1. Grupo de Recursos
echo "Criando Grupo de Recursos: $RESOURCE_GROUP"
az group create --name $RESOURCE_GROUP --location $LOCATION

# 2. Storage Account (para os arquivos e para a Function)
echo "Criando Storage Account: $STORAGE_ACCOUNT"
az storage account create --name $STORAGE_ACCOUNT --location $LOCATION --resource-group $RESOURCE_GROUP --sku Standard_LRS

# 3. Cosmos DB (Conta Serverless)
echo "Criando Conta do Cosmos DB: $COSMOSDB_ACCOUNT"
az cosmosdb create --name $COSMOSDB_ACCOUNT --resource-group $RESOURCE_GROUP --locations "primaryLocation=$LOCATION" --capabilities "EnableServerless"

# 4. Cosmos DB (Banco de Dados e Contêiner)
echo "Criando Banco de Dados e Contêiner no Cosmos DB"
az cosmosdb sql database create --account-name $COSMOSDB_ACCOUNT --resource-group $RESOURCE_GROUP --name "ServerlessDB"
az cosmosdb sql container create --account-name $COSMOSDB_ACCOUNT --resource-group $RESOURCE_GROUP --database-name "ServerlessDB" --name "Items" --partition-key-path "/id"

# 5. Function App
echo "Criando Function App: $FUNCTION_APP_NAME"
az functionapp create --name $FUNCTION_APP_NAME \
  --storage-account $STORAGE_ACCOUNT \
  --consumption-plan-location $LOCATION \
  --resource-group $RESOURCE_GROUP \
  --runtime python \
  --runtime-version 3.9 \
  --functions-version 4 \
  --os-type linux

echo "--- Infraestrutura criada com sucesso! ---"
```

---

## 💻 2. Configuração Local

1.  **Clone o repositório** e navegue até a pasta raiz.
2.  **Crie e ative um ambiente virtual**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # No Windows: .venv\Scripts\activate
    ```
3.  **Instale as dependências**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure as conexões**:
    -   Renomeie `local.settings.json.template` para `local.settings.json`.
    -   Execute os comandos abaixo para obter as chaves de conexão e cole-as no arquivo:

    ```bash
    # Obter Connection String do Storage Account
    az storage account show-connection-string --name $STORAGE_ACCOUNT --resource-group $RESOURCE_GROUP --query "connectionString"

    # Obter Connection String do Cosmos DB
    az cosmosdb keys list --name $COSMOSDB_ACCOUNT --resource-group $RESOURCE_GROUP --type "connection-strings" --query "connectionStrings[0].connectionString"
    ```
5.  **Inicie o projeto localmente**:
    ```bash
    func start
    ```

---

## 🚀 3. Deploy para a Azure

1.  **Faça login com a Azure Functions Core Tools**:
    ```bash
    func azure login
    ```
2.  **Publique o projeto**:
    ```bash
    func azure functionapp publish $FUNCTION_APP_NAME --python
    ```
    O processo de deploy irá configurar automaticamente as conexões (`AzureWebJobsStorage` e `CosmosDbConnectionString`) nas configurações da sua aplicação na nuvem.

---

## 🧪 4. Testando as APIs

Após o deploy, o terminal mostrará as URLs dos seus endpoints. Você precisará de uma chave de API para chamá-los.

-   **Como obter a chave de API**:
    Vá para o Portal da Azure -> seu Function App -> Funções -> `SuaFuncao` -> `Chaves de função e host`. Copie o valor da chave `_master` ou `default`.

-   **Use `curl` ou outra ferramenta de API para testar**:

**1. Upload de Arquivo** (crie um arquivo `teste.txt` antes)
```bash
curl -X POST \
  -F "file=@./teste.txt" \
  "https://<SEU_APP_NAME>.azurewebsites.net/api/files/upload?code=<SUA_CHAVE>"
```

**2. Criar Documento**
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"id": "1", "name": "Produto A", "category": "tecnologia"}' \
  "https://<SEU_APP_NAME>.azurewebsites.net/api/documents?code=<SUA_CHAVE>"
```
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"id": "2", "name": "Livro B", "category": "literatura"}' \
  "https://<SEU_APP_NAME>.azurewebsites.net/api/documents?code=<SUA_CHAVE>"
```

**3. Listar Todos os Documentos**
```bash
curl "https://<SEU_APP_NAME>.azurewebsites.net/api/documents?code=<SUA_CHAVE>"
```

**4. Filtrar Documentos por Categoria**
```bash
curl "https://<SEU_APP_NAME>.azurewebsites.net/api/documents/filter?category=tecnologia&code=<SUA_CHAVE>"
```
