from flask import Flask, request, jsonify
from flask_cors import CORS
from coleta.rag_agent import ask_bot

# --- Inicialização ---
print("Inicializando o servidor Flask...")
app = Flask(__name__)
# Habilita o CORS para permitir que seu frontend (de outra origem) acesse esta API
CORS(app)

print("Carregando o agente de IA... Isso pode levar um momento.")
# Carregar o agente de IA (agora ask_bot direto)
try:
    # ask_bot agora é uma função que usa Supabase diretamente
    agent = None  # Não precisa mais de agente LangChain
    print("Agente de IA carregado com sucesso (modo Supabase direto).")
except Exception as e:
    print(f"Erro ao carregar agente: {e}")
    agent = None

# --- Definição do Endpoint da API ---
@app.route('/ask', methods=['POST'])
def handle_ask():
    """
    Endpoint para receber perguntas do frontend e retornar respostas do agente de IA.
    """
    data = request.get_json()
    print(f"Dados recebidos: {data}")
    if not data or 'question' not in data:
        print("Erro: dados inválidos ou 'question' ausente")
        return jsonify({"error": "A pergunta não foi fornecida no corpo da requisição."}), 400

    user_question = data['question']
    print(f"\nRecebida pergunta do frontend: '{user_question}'")

    # Usar ask_bot direto
    bot_response = ask_bot(user_question)

    print(f"Enviando resposta para o frontend: '{bot_response}'")
    return jsonify({"answer": bot_response})

# --- Execução do Servidor ---
if __name__ == '__main__':
    # Executa o servidor na porta 5000, acessível na sua rede local
    app.run(host='0.0.0.0', port=5000, debug=False)
