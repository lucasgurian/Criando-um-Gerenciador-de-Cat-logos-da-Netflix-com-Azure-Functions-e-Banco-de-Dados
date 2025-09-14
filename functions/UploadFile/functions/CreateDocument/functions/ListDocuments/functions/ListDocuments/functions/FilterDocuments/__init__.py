import logging
import json
import azure.functions as func

def main(req: func.HttpRequest, documents: func.DocumentList) -> func.HttpResponse:
    """
    Função para filtrar documentos no Cosmos DB com base em um parâmetro 'category'.
    """
    logging.info('Função FilterDocuments processando uma requisição.')

    category = req.params.get('category')
    if not category:
        return func.HttpResponse("Por favor, forneça o parâmetro 'category' na query string.", status_code=400)

    if not documents:
        return func.HttpResponse(f"Nenhum documento encontrado para a categoria '{category}'.", status_code=404)

    docs_json = [json.loads(doc.to_json()) for doc in documents]

    return func.HttpResponse(
        body=json.dumps(docs_json),
        mimetype="application/json",
        status_code=200
    )
