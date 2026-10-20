import oracledb

class Conexaodb: # classe responsável por guardar os dados de conexão e criar a conexão com o banco de dados Oracle


    # contrutor: roda automaticamente quando criamos um objeto Conexaodb(...)
    # recebe os dados necessários para conectar com o Oracle 
    def __init__(self, usuario, senha, host, porta, service_name):
        # guarda cada dado recebido dentro do objeto (self) para usar em outro método
        self.usuario = usuario
        self.senha = senha
        self.host = host
        self.porta = porta
        self.service_name = service_name

        # monta o dsn que é obrigatório pra conectar com o Oracle 
        # é basicamente o "endereço completo" do banco de dados, incluindo host, porta e service_name
        self.dsn = oracledb.makedsn(
            host,
            porta,
            service_name=service_name
        )

    # método que de fato inicia a conexão com o banco de dados Oracle 
    def conectar(self):
        # tenta executar o código de conexão, se der erro, cai no except
        try:
            # abre a conexao usando as informações do self que foi guardado no contrutor (linha 11)
            conn = oracledb.connect(
                user=self.usuario,
                password=self.senha,
                dsn=self.dsn
            )
            # retorna a conexão aberta para quem chamou o construtor
            return conn

        # tratamento de erro caso a conexão falhe, exibe o erro e retorna None
        except oracledb.Error as erro:
            print("Erro ao se conectar ao Oracle:", erro)
            return None
