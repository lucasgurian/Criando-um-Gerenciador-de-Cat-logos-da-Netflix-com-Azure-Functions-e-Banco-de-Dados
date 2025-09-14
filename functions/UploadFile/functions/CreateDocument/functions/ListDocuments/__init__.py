import logging
import json
import azure.functions as func

def main(req: func.HttpRequest, documents: func.DocumentList) -> func.HttpResponse:
    """
    Função para listar todos os documentos do Cosmos DB.
    """
    logging.info('Função ListDocuments processando uma requisição.')

    if not documents:
        return func.HttpResponse("Nenhum documento encontrado.", status_code=404)

    # Converte a lista de documentos para um formato JSON serializável
    docs_json = [json.loads(doc.to_json()) for doc in documents]

    return func.HttpResponse(
        body=json.dumps(docs_json),
        mimetype="application/json",
        status_code=200
    )
