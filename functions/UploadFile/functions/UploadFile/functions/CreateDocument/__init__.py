import logging
import json
import azure.functions as func

def main(req: func.HttpRequest, doc: func.Out[func.Document]) -> func.HttpResponse:
    """
    Função para criar um novo documento no Cosmos DB.
    Espera um corpo de requisição em formato JSON.
    """
    logging.info('Função CreateDocument processando uma requisição.')

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse("Corpo da requisição inválido. Por favor, envie um JSON.", status_code=400)

    # O binding 'doc' salva o JSON diretamente no Cosmos DB
    doc.set(func.Document.from_json(json.dumps(req_body)))

    return func.HttpResponse(
        body=json.dumps({"status": "Documento criado com sucesso", "data": req_body}),
        mimetype="application/json",
        status_code=201
    )
