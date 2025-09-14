import logging
import azure.functions as func

def main(req: func.HttpRequest, outblob: func.Out[bytes]) -> func.HttpResponse:
    """
    Função para fazer upload de um arquivo para o Azure Blob Storage.
    Espera uma requisição multipart/form-data com um campo 'file'.
    """
    logging.info('Função UploadFile processando uma requisição.')

    try:
        # Busca o arquivo na requisição
        file = req.files.get('file')
        if not file:
            return func.HttpResponse(
                "Nenhum arquivo encontrado. Por favor, envie um arquivo no campo 'file' do formulário.",
                status_code=400
            )

        # O nome do arquivo original será usado como nome do blob
        filename = file.filename
        file_bytes = file.read()

        # O binding 'outblob' salva o conteúdo no storage
        outblob.set(file_bytes)

        logging.info(f"Arquivo '{filename}' salvo com sucesso no blob storage.")

        return func.HttpResponse(
            f"Arquivo '{filename}' enviado com sucesso!",
            status_code=200
        )

    except Exception as e:
        logging.error(f"Erro ao processar o upload: {e}")
        return func.HttpResponse("Erro interno ao processar o arquivo.", status_code=500)
