class Evento:
    def __init__(
        self,
        id_evento,
        nome_evento,
        categoria,
        data_evento,
        local_evento,
        capacidade,
        valor_ingresso,
        responsavel,
        status,
        data_cadastro,
    ):
        self.id_evento = id_evento
        self.nome_evento = nome_evento
        self.categoria = categoria
        self.data_evento = data_evento
        self.local_evento = local_evento
        self.capacidade = capacidade
        self.valor_ingresso = valor_ingresso
        self.responsavel = responsavel
        self.status = status
        self.data_cadastro = data_cadastro

    def to_dict(self):
        return {
            "id_evento": self.id_evento,
            "nome_evento": self.nome_evento,
            "categoria": self.categoria,
            "data_evento": self.data_evento,
            "local_evento": self.local_evento,
            "capacidade": self.capacidade,
            "valor_ingresso": self.valor_ingresso,
            "responsavel": self.responsavel,
            "status": self.status,
            "data_cadastro": self.data_cadastro,
        }
