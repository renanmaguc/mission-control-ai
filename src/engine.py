"""
Motor de análise da Mission Control AI.
"""

import os

from ollama import Client
from dotenv import load_dotenv

from pathlib import Path

from src.telemetria import coletar
from src.alertas import avaliar


load_dotenv()


# Identificação da trilha
TRILHA = "connectsat"


client = Client(
    host="https://ollama.com",
    headers={
        'Authorization': 'Bearer ' + os.environ.get(
            'OLLAMA_API_KEY',
            ''
        )
    }
)


def llm(
    prompt,
    system=None,
    max_tokens=800,
    temperature=0.3
):
    """
    Envia prompt ao gpt-oss:120b via Ollama Cloud.
    """

    messages = []

    if system:

        messages.append({
            "role": "system",
            "content": system
        })

    messages.append({
        "role": "user",
        "content": prompt
    })

    try:

        return client.chat(
            model="gpt-oss:120b",
            messages=messages,
            options={
                "num_predict": max_tokens,
                "temperature": temperature
            },
            stream=False
        )['message']['content'].strip()

    except Exception as e:

        return f"⚠️ Erro ao consultar IA: {e}"


def load_system_prompt():
    """
    Lê o system prompt do arquivo
    prompts/system_prompt.md
    """

    path = Path("prompts/system_prompt.md")

    if path.exists():

        return path.read_text(
            encoding="utf-8"
        )

    return "Você é um assistente."


class MissionEngine:
    """
    Motor de análise da missão.
    """

    def __init__(self):

        self.trilha = TRILHA

        self.system_prompt = load_system_prompt()

    def is_ready(self):

        return True

    def status_snapshot(self):
        """
        Retorna estado atual da telemetria.
        """

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
        """
        Analisa pergunta usando:
        telemetria + alertas + IA.
        """

        # 1. Coletar dados
        dados = coletar()

        # 2. Avaliar alertas
        alertas = avaliar(dados)

        # Formata alertas
        alertas_texto = "\n".join(alertas)

        # 3. Montar prompt
        prompt = f"""
DADOS DA MISSÃO:

Temperatura: {dados['temperatura']}°C
Energia: {dados['energia']}%
Comunicação: {dados['comunicacao']}
Latência: {dados['latencia']} ms
Estabilidade: {dados['estabilidade']}%

ALERTAS DETECTADOS:
{alertas_texto}

PERGUNTA DO OPERADOR:
{pergunta_usuario}

Analise:
- riscos
- severidade
- impacto operacional
- impacto terrestre
- recomendação operacional
"""

        # 4. Chamar IA
        resposta = llm(
            prompt,
            system=self.system_prompt
        )

        # 5. Retornar resposta
        return resposta