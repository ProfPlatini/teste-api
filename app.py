from flask import Flask,jsonify,request
from flask_cors import CORS
from agno.models.openai import OpenAIChat
from agno.agent import Agent
from dotenv import load_dotenv
import os #Os permite ler as variáveis do .evn
from supabase import create_client #Função que permite conectar no banco

#Lendo a nossa API KEY que está no .env
load_dotenv()
#Criando o nosso app
app = Flask(__name__)
#Permitindo acessos externos
CORS(app)

#Pegar o endereço e a chave do banco que está no .env
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
                         
supabase = create_client(supabase_url,supabase_key) #Para criar a conexão com o banco, informo a URL e a KEY que estão armazenadas no .env.

agente = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    description="Você é uma assistente útil e prestativa do Hotel Travesseiro Nervoso"
    "Você ajuja os hóspedes a encontrar o melhor quarto possível baseado no que estão procurando"
    "Você responde de forma clara e objetiva informações relevantes sobre quartos,serviços, reservas e políticas da empresa"
    "Você utiliza um tom amigável e levemente humorado"
    "Quarto Standard($600), Quarto Deluxe($700),Quarto Suíte($1000)"
)

#Criar  o método GET para testar a API
@app.route("/chat", methods=['GET'])
def testarAPI():
    return jsonify({"mensagem":"API funcionando corretamente"}),200

#Criar o método de enviar a pergunta
@app.route("/chat", methods=['POST'])
def enviarPergunta():
    dados = request.get_json()
    pergunta = dados['pergunta']
    resposta = agente.run(pergunta)
    return jsonify({"mensagem":resposta.content})

#Criar método para receber a reserva e salvar no banco de dados
@app.route("/reservar", methods=['POST'])
def reservar():
    dados = request.get_json()
    
    #Agora, preciso organizar esses dados em um dicionário, com as mesmas colunas da tabela do banco de dados
    nova_reserva = {
        "nome":dados["nome"],
        "email":dados["email"],
        "tipo_quarto":dados["tipo_quarto"],
        "checkin":dados["checkin"]
    }
    
    #Agora, comando para reservar os dados na tabela do banco
    supabase.table("reservas").insert(nova_reserva).execute()
    
    return jsonify({"mensagem":"Reserva realizada com sucesso!"})

#Iniciando o nosso app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
