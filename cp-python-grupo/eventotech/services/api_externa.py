import requests

def verificar_feriado(data_evento):
    try:
        ano = data_evento.year
        url = f"https://brasilapi.com.br/api/feriados/v1/{ano}"
        resposta = requests.get(url, timeout=5)
        resposta.raise_for_status()
        feriados = resposta.json()

    except requests.Timeout:
        return {"erro": "Tempo limite excedido ao consultar feriados"}
    except requests.ConnectionError:
        return {"erro": "Não foi possível conectar à API de feriados"}
    except requests.exceptions.JSONDecodeError:
        return {"erro": "Resposta da API em formato inválido"}