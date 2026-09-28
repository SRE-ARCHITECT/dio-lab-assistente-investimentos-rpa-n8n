"""
Robotic Process Automation (RPA) - Extração de Clientes e Disparo ao n8n
DIO Lab: Assistente de Investimentos com RPA e IA Generativa

Autor: SRE-ARCHITECT
Dev: https://webappdesigner.com.br
"""

import os
import sys
import json
import logging
import requests
from bs4 import BeautifulSoup

# Configuração de Logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("RPA_Investimentos")

URL_PAGINA_PADRAO = "https://digitalinnovationone.github.io/dio-lab-assistente-investimentos-rpa-n8n/"
N8N_WEBHOOK_PADRAO = os.getenv("N8N_WEBHOOK_URL", "http://localhost:5678/webhook/clientes")


def extrair_clientes(url_ou_caminho: str = URL_PAGINA_PADRAO) -> list[dict]:
    """
    RPA: Acessa a página HTML, localiza a tabela #clientes e extrai os registros.
    Suporta tanto URL web quanto arquivo HTML local (fallback offline).
    """
    logger.info(f"Iniciando coleta de dados em: {url_ou_caminho}")
    html_content = ""

    # Suporte para URL remota ou arquivo local
    if url_ou_caminho.startswith("http://") or url_ou_caminho.startswith("https://"):
        try:
            resposta = requests.get(url_ou_caminho, timeout=10)
            resposta.raise_for_status()
            html_content = resposta.text
            logger.info("Página web carregada com sucesso.")
        except requests.RequestException as err:
            logger.warning(f"Falha ao acessar URL remota ({err}). Tentando arquivo local de fallback...")
            caminho_local = os.path.join(os.path.dirname(__file__), "..", "docs", "index.html")
            if os.path.exists(caminho_local):
                with open(caminho_local, "r", encoding="utf-8") as f:
                    html_content = f.read()
                logger.info(f"Fallback local utilizado com sucesso: {caminho_local}")
            else:
                logger.error("Nenhuma fonte de dados acessível.")
                raise
    else:
        with open(url_ou_caminho, "r", encoding="utf-8") as f:
            html_content = f.read()

    soup = BeautifulSoup(html_content, "html.parser")
    linhas = soup.select("#clientes tbody tr")

    if not linhas:
        logger.warning("Nenhuma linha de cliente encontrada na tabela #clientes.")
        return []

    clientes = []
    for linha in linhas:
        colunas = linha.find_all("td")
        if len(colunas) >= 4:
            cliente = {
                "nome": colunas[0].get_text(strip=True),
                "email": colunas[1].get_text(strip=True),
                "saldo": colunas[2].get_text(strip=True),
                "perfil": colunas[3].get_text(strip=True)
            }
            clientes.append(cliente)

    logger.info(f"Total de {len(clientes)} clientes extraídos com sucesso.")
    return clientes


def enviar_ao_n8n(clientes: list[dict], webhook_url: str = N8N_WEBHOOK_PADRAO) -> bool:
    """
    Envia a lista consolidada de clientes extraídos para o Webhook do n8n via POST.
    """
    if not clientes:
        logger.warning("Lista de clientes vazia. Disparo cancelado.")
        return False

    payload = {"clientes": clientes}
    logger.info(f"Enviando {len(clientes)} clientes para o Webhook do n8n: {webhook_url}")

    try:
        resp = requests.post(
            webhook_url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=15
        )
        if resp.status_code in [200, 201]:
            logger.info(f"Sucesso! n8n respondeu com status {resp.status_code}: {resp.text}")
            return True
        else:
            logger.warning(f"O webhook n8n retornou status {resp.status_code}: {resp.text}")
            return False
    except requests.exceptions.ConnectionError:
        logger.warning(
            f"Não foi possível conectar ao n8n em {webhook_url}. "
            "Certifique-se de que o workflow no n8n está Ativo ou em modo 'Test Step'."
        )
        return False
    except Exception as err:
        logger.error(f"Erro inesperado no envio ao webhook: {err}")
        return False


def main():
    print("=" * 60)
    print("🤖 RPA DIO: Extrator de Clientes para Assistente n8n + IA")
    print("=" * 60)

    # 1. Extração
    clientes = extrair_clientes()

    # 2. Exibição
    print("\n📋 Clientes Extraídos:")
    for idx, c in enumerate(clientes, 1):
        print(f"  {idx}. {c['nome']} | {c['email']} | Saldo: {c['saldo']} | Perfil: {c['perfil']}")

    # 3. Disparo ao Webhook
    webhook_target = sys.argv[1] if len(sys.argv) > 1 else N8N_WEBHOOK_PADRAO
    print(f"\n🌐 Alvo do Webhook: {webhook_target}")
    sucesso = enviar_ao_n8n(clientes, webhook_target)

    if sucesso:
        print("\n✅ Fluxo de RPA executado com êxito de ponta a ponta!")
    else:
        print("\nℹ️  Dados extraídos com sucesso. Configure a URL real do n8n para disparo contínuo.")


if __name__ == "__main__":
    main()
