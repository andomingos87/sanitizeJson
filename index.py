import logging
from flask import Flask, request, Response

app = Flask(__name__)

# Configuração básica do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def sanitize_message(message):
    """
    Escapa caracteres problemáticos em uma string para que seja aceita como JSON válido.
    """
    if not message:
        logging.warning("A mensagem recebida é vazia ou None.")
        return ""

    sanitized_message = (
        message.replace("\\", "\\\\")  # Escapar barras invertidas
               .replace("\"", "\\\"")  # Escapar aspas duplas
               .replace("\n", "\\n")   # Escapar quebras de linha
               .replace("\r", "\\r")   # Escapar retornos de carro
               .replace("\t", "\\t")   # Escapar tabulações
    )

    logging.debug(f"Mensagem original: {message}")
    logging.debug(f"Mensagem sanitizada: {sanitized_message}")

    return sanitized_message

@app.route('/sanitize', methods=['POST'])
def sanitize():
    """
    Endpoint que sanitiza mensagens recebidas no formato JSON e retorna texto puro.
    """
    try:
        logging.info("Requisição recebida no endpoint /sanitize.")

        # Receber a mensagem enviada
        data = request.get_json()
        logging.debug(f"Dados recebidos: {data}")

        if not data:
            logging.error("Nenhum dado JSON foi fornecido na requisição.")
            return Response("Requisição inválida, JSON é obrigatório.", status=400, mimetype='text/plain')

        if "message" not in data:
            logging.error("A chave 'message' não está presente no JSON recebido.")
            return Response("Requisição inválida, 'message' é obrigatório.", status=400, mimetype='text/plain')

        message = data["message"]
        logging.info("Mensagem recebida para sanitização.")

        # Sanitizar a mensagem
        sanitized = sanitize_message(message)

        # Retornar a mensagem sanitizada como texto puro
        logging.info("Mensagem sanitizada com sucesso.")
        return Response(sanitized, status=200, mimetype='text/plain')

    except Exception as e:
        logging.exception("Ocorreu um erro inesperado no endpoint /sanitize.")
        return Response(str(e), status=500, mimetype='text/plain')

if __name__ == '__main__':
    # Configurar o logger para exibir mensagens no console
    logging.getLogger().setLevel(logging.DEBUG)
    app.run(host='0.0.0.0', port=5001)
