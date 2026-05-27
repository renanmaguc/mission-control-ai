"""
Interface CLI estilo Mission Control
usa Rich + prompt-toolkit
"""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style

import pyfiglet

from datetime import datetime


console = Console()

session = PromptSession(
    style=Style.from_dict({
        "prompt": "#8B5CF6 bold"
    })
)


def show_banner():
    """
    Exibe banner ASCII colorido no início
    """

    banner = pyfiglet.figlet_format(
        "Orbit Watch",
        font="slant"
    )

    console.print(
        Text(
            banner,
            style="bold #8B5CF6"
        )
    )

    console.print(
        Panel.fit(
            "Sistema inteligente de monitoramento orbital.\n"
            "Use /help para ver os comandos · /exit para sair.\n"
            "IA: gpt-oss:120b via Ollama Cloud",

            title="◆ ORBIT WATCH",

            border_style="#8B5CF6"
        )
    )


def show_response(text):
    """
    Renderiza resposta da IA
    """

    now = datetime.now().strftime("%H:%M")

    console.print(
        Panel(
            text,

            title="◆ Mission Analysis",

            subtitle=now,

            border_style="#8B5CF6"
        )
    )


def run_cli(engine):
    """
    Loop principal da CLI
    """

    show_banner()

    if not engine.is_ready():

        console.print(
            "⚠ Engine status: OFFLINE\n",
            style="bold yellow"
        )

    while True:

        try:

            user_input = session.prompt("❯ ").strip()

        except (KeyboardInterrupt, EOFError):

            break

        if not user_input:

            continue

        # SAIR
        if user_input == "/exit":

            break

        # AJUDA
        if user_input == "/help":

            console.print(
                """
Comandos disponíveis:

/help   → ajuda
/status → status da missão
/about  → sobre o sistema
/clear  → limpar terminal
/exit   → sair
"""
            )

            continue

        # STATUS
        if user_input == "/status":

            show_response(
                engine.status_snapshot()
            )

            continue

        # SOBRE
        if user_input == "/about":

            show_response(
                """
Orbit Watch AI

Sistema de monitoramento espacial
com inteligência artificial generativa.

Desenvolvido para análise:
- telemetria orbital
- falhas críticas
- riscos operacionais
- impacto terrestre
"""
            )

            continue

        # LIMPAR
        if user_input == "/clear":

            console.clear()

            show_banner()

            continue

        # CONSULTA IA
        resposta = engine.analyze(user_input)

        show_response(resposta)