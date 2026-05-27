import os
from ollama import Client
from dotenv import load_dotenv
import time
from datetime import datetime

from src.telemetria import coletar
from src.alertas import avaliar

load_dotenv()

client = Client(
    host="https://ollama.com",
    headers={
        "Authorization": "Bearer " + os.environ.get("OLLAMA_API_KEY")
    }
)

# Teste da API Key
api = os.environ.get("OLLAMA_API_KEY")

print(
    "API KEY carregada:",
    "OK" if api else "FALTANDO"
)


def llm(prompt, max_tokens=800, temperature=0.3):
    """
    Envia prompt ao gpt-oss:120b via Ollama Cloud
    e retorna texto.
    """

    try:

        resposta = client.chat(
            model="gpt-oss:120b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            options={
                "num_predict": max_tokens,
                "temperature": temperature
            },
            stream=False
        )

        return resposta["message"]["content"].strip()

    except Exception as e:

        return f"⚠️ Erro ao consultar IA: {e}"


class MissionEngine:

    def __init__(self):

        self.system_prompt = self.load_system_prompt()

    def load_system_prompt(self):

        try:

            with open(
                "prompts/system_prompt.md",
                "r",
                encoding="utf-8"
            ) as arquivo:

                return arquivo.read()

        except:

            return """
Você é um engenheiro especialista em monitoramento
de missões espaciais.

Analise os dados da missão e forneça:
- diagnóstico
- severidade
- impacto operacional
- impacto terrestre
- recomendações
"""

    def is_ready(self):

        return api is not None

    def status_snapshot(self):

        dados = coletar()

        return f"""
===== STATUS DA MISSÃO =====

Temperatura: {dados['temperatura']}°C
Energia: {dados['energia']}%
Comunicação: {dados['comunicacao']}
Latência: {dados['latencia']} ms
Estabilidade: {dados['estabilidade']}%

============================
"""

    def analyze(self, pergunta_usuario):

        # Coleta telemetria
        dados = coletar()

        # Detecta alertas
        alertas = avaliar(dados)

        # Prompt dinâmico
        prompt = f"""
{self.system_prompt}

DADOS ATUAIS DA MISSÃO:

Temperatura: {dados['temperatura']}°C
Energia: {dados['energia']}%
Comunicação: {dados['comunicacao']}
Latência: {dados['latencia']} ms
Estabilidade: {dados['estabilidade']}%

ALERTAS DETECTADOS:
{alertas}

PERGUNTA DO OPERADOR:
{pergunta_usuario}

Forneça:
1. Diagnóstico da missão
2. Problemas encontrados
3. Severidade dos riscos
4. Impacto na Terra
5. Recomendação operacional
"""

        resposta = llm(prompt)

        return resposta