from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
import string
import random
import secrets
import logging


logging.basicConfig(level=logging.INFO)

app = Flask(__name__)


CORS(app)
app.logger.info("CORS configurado para permitir todas as origens.")


DEFAULT_LIMIT_VALUES = ["200 per day", "50 per hour", "10 per minute"]

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=DEFAULT_LIMIT_VALUES,
    storage_uri="memory://",
)
app.logger.info(f"Flask-Limiter configurado com limites padrão: {DEFAULT_LIMIT_VALUES}")


def gerar_senha_segura(
    comprimento, usar_maiusculas, usar_minusculas, usar_numeros, usar_simbolos
):
    """Gera uma senha segura com base nos critérios fornecidos."""
    caracteres = ""
    senha_gerada_lista = []

    if not (usar_maiusculas or usar_minusculas or usar_numeros or usar_simbolos):

        raise ValueError("Pelo menos um tipo de caractere deve ser selecionado.")

    if usar_maiusculas:
        caracteres += string.ascii_uppercase
        senha_gerada_lista.append(secrets.choice(string.ascii_uppercase))
    if usar_minusculas:
        caracteres += string.ascii_lowercase
        senha_gerada_lista.append(secrets.choice(string.ascii_lowercase))
    if usar_numeros:
        caracteres += string.digits
        senha_gerada_lista.append(secrets.choice(string.digits))
    if usar_simbolos:

        caracteres += string.punctuation
        senha_gerada_lista.append(secrets.choice(string.punctuation))

    if not caracteres:
        app.logger.error(
            "Nenhum conjunto de caracteres foi formado, apesar das seleções."
        )
        raise ValueError(
            "Erro interno: Nenhum conjunto de caracteres válido foi formado."
        )

    if comprimento < len(senha_gerada_lista):
        senha_gerada_lista = random.sample(senha_gerada_lista, comprimento)
    else:

        comprimento_restante = comprimento - len(senha_gerada_lista)
        for _ in range(comprimento_restante):
            senha_gerada_lista.append(secrets.choice(caracteres))

    random.shuffle(senha_gerada_lista)
    senha_final = "".join(senha_gerada_lista)
    app.logger.info(f"Senha gerada com comprimento {len(senha_final)}.")
    return senha_final


@app.route("/gerar_senha", methods=["POST"])
@limiter.limit("5 per minute")
def api_gerar_senha():
    app.logger.info(
        f"Requisição recebida em /gerar_senha de {request.remote_addr} com método {request.method}"
    )

    if request.method == "POST":
        try:
            dados = request.get_json()
            if not dados:
                app.logger.warning("Requisição POST sem dados JSON.")
                return (
                    jsonify({"erro": "Corpo da requisição JSON ausente ou inválido."}),
                    400,
                )

            app.logger.info(f"Dados recebidos: {dados}")

            comprimento = dados.get("comprimento")
            usar_maiusculas = bool(dados.get("maiusculas", False))
            usar_minusculas = bool(dados.get("minusculas", False))
            usar_numeros = bool(dados.get("numeros", False))
            usar_simbolos = bool(dados.get("simbolos", False))

            if not isinstance(comprimento, int) or not (8 <= comprimento <= 128):
                app.logger.warning(
                    f"Tentativa de gerar senha com comprimento inválido: {comprimento}"
                )
                return (
                    jsonify(
                        {
                            "erro": "Comprimento inválido. Deve ser um número entre 8 e 128."
                        }
                    ),
                    400,
                )

            if not (
                usar_maiusculas or usar_minusculas or usar_numeros or usar_simbolos
            ):
                app.logger.warning("Nenhum tipo de caractere selecionado.")
                return (
                    jsonify({"erro": "Selecione pelo menos um tipo de caractere."}),
                    400,
                )

            senha = gerar_senha_segura(
                comprimento,
                usar_maiusculas,
                usar_minusculas,
                usar_numeros,
                usar_simbolos,
            )
            app.logger.info(f"Senha gerada com sucesso para {request.remote_addr}.")
            return jsonify({"senha": senha}), 200

        except ValueError as ve:
            app.logger.error(f"ValueError ao processar requisição: {str(ve)}")
            return jsonify({"erro": str(ve)}), 400
        except Exception as e:
            app.logger.error(f"Erro inesperado ao gerar senha: {e}", exc_info=True)
            return (
                jsonify(
                    {"erro": "Ocorreu um erro interno no servidor ao gerar a senha."}
                ),
                500,
            )
    else:

        app.logger.warning(
            f"Método {request.method} não permitido para /gerar_senha de {request.remote_addr}."
        )
        return jsonify({"erro": "Método não permitido."}), 405


@limiter.limit("5 per minute")
def api_gerar_senha():

    app.logger.info(
        f"Requisição recebida em /gerar_senha de {request.remote_addr} com método {request.method}"
    )

    if request.method == "POST":
        try:
            dados = request.get_json()
            if not dados:
                app.logger.warning("Requisição POST sem dados JSON.")
                return (
                    jsonify({"erro": "Corpo da requisição JSON ausente ou inválido."}),
                    400,
                )

            app.logger.info(f"Dados recebidos: {dados}")

            comprimento = dados.get("comprimento")
            usar_maiusculas = bool(dados.get("maiusculas", False))
            usar_minusculas = bool(dados.get("minusculas", False))
            usar_numeros = bool(dados.get("numeros", False))
            usar_simbolos = bool(dados.get("simbolos", False))

            if not isinstance(comprimento, int) or not (8 <= comprimento <= 128):
                app.logger.warning(
                    f"Tentativa de gerar senha com comprimento inválido: {comprimento}"
                )
                return (
                    jsonify(
                        {
                            "erro": "Comprimento inválido. Deve ser um número entre 8 e 128."
                        }
                    ),
                    400,
                )

            if not (
                usar_maiusculas or usar_minusculas or usar_numeros or usar_simbolos
            ):
                app.logger.warning("Nenhum tipo de caractere selecionado.")
                return (
                    jsonify({"erro": "Selecione pelo menos um tipo de caractere."}),
                    400,
                )

            senha = gerar_senha_segura(
                comprimento,
                usar_maiusculas,
                usar_minusculas,
                usar_numeros,
                usar_simbolos,
            )
            app.logger.info(f"Senha gerada com sucesso para {request.remote_addr}.")
            return jsonify({"senha": senha}), 200

        except ValueError as ve:
            app.logger.error(f"ValueError ao processar requisição: {str(ve)}")
            return jsonify({"erro": str(ve)}), 400
        except Exception as e:

            app.logger.error(f"Erro inesperado ao gerar senha: {e}", exc_info=True)
            return (
                jsonify(
                    {"erro": "Ocorreu um erro interno no servidor ao gerar a senha."}
                ),
                500,
            )
    else:

        return jsonify({"erro": "Método não permitido."}), 405


@app.route("/")
def index():
    app.logger.info(f"Acesso à rota raiz de {request.remote_addr}")
    return jsonify({"mensagem": "Servidor do Gerador de Senhas está no ar!"})


if __name__ == "__main__":

    app.logger.info("Iniciando servidor Flask em modo de desenvolvimento.")
    app.run(debug=True, host="0.0.0.0", port=5000)
