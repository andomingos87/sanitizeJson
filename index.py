from flask import Flask, request, jsonify

app = Flask(__name__)

def sanitize_message(message):
    """
    Escapa caracteres problemáticos em uma string para que seja aceita como JSON válido.
    """
    if not message:
        return ""

    sanitized_message = (
        message.replace("\\", "\\\\")   # Escapar barras invertidas
               .replace("\"", "\\\"")   # Escapar aspas duplas
               .replace("\n", "\\n")    # Escapar quebras de linha
               .replace("\r", "\\r")    # Escapar retornos de carro
               .replace("\t", "\\t")    # Escapar tabulações
    )

    return sanitized_message

@app.route('/sanitize', methods=['POST'])
def sanitize():
    """
    Endpoint que sanitiza mensagens recebidas no formato JSON.
    """
    try:
        # Receber a mensagem enviada
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"error": "Requisição inválida, 'message' é obrigatório."}), 400

        message = data["message"]

        # Sanitizar a mensagem
        sanitized = sanitize_message(message)

        # Retornar a mensagem sanitizada
        return jsonify({"sanitizedMessage": sanitized}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
