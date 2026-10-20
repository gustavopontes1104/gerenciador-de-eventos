import requests


def verificar_feriado(data_evento):
    try:
        ano = data_evento.year
        url = f"https://brasilapi.com.br/api/feriados/v1/{ano}"
        resposta = requests.get(url, timeout=5)
        resposta.raise_for_status()
        feriados = resposta.json()

        data_str = data_evento.strftime("%Y-%m-%d")
        for feriado in feriados:
            if feriado.get("date") == data_srt:
                return {"eh_feriado": True, "nome_feriado": feriado.get("name")}

        return {"eh_feriado": False, "nome_feriado": None}

    except requests.Timeout:
        return {"erro": "Tempo limite excedido ao consultar feriados"}
    except requests.ConnectionError:
        return {"erro": "Não foi possível conectar à API de feriados"}
    except requests.exceptions.HTTPError:
        return {"erro": "Erro HTTP ao consultar API de feriados"}
    except requests.exceptions.JSONDecodeError:
        return {"erro": "Resposta da API em formato inválido"}
    except Exception as e:
        return {"erro": f"Erro inesperado: {e}"}
