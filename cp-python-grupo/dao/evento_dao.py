from connOracle.conndb import Conexaodb
import oracledb

# dao significa Data Access Object, classe concentra TODO o o acesso ao banco de dados
class EventoDAO:
    # classe: roda ao criar um EventoDAO(), guarda a conexão
    def __init__(self):
        # cria o objeto de conexão com o banco de dados usando a classe Conexaodb (localizada em connOracle/conndb.py)
        # guarda os dados mas não abre a conexão, quem abre é o método conectar() da classe Conexaodb (localizada em connOracle/conndb.py   )
        self.conexao = Conexaodb(
            # dados de conexão
            usuario="rm569961",
            senha="030308",
            host="host",
            porta=1521,
            service_name="ORCL",
        )

    # recebe um objeto evento (da classe Evento) e insere no banco de dados
    def cadastrar_evento(self, evento):
        # abre conexão com o banco de dados usando o método conectar() da classe Conexaodb (localizada em connOracle/conndb.py) // devolve None se falhar
        conn = self.conexao.conectar()
        # se não conseguir conectar, exibe mensagem de erro e retorna False
        if conn is None:
            print("Erro ao conectar ao Oracle.")
            return False

        # copia os atributos do objeto Evento em variáveis para usar na query SQL
        id_evento = evento.id_evento
        nome_evento = evento.nome_evento
        categoria = evento.categoria
        data_evento = evento.data_evento
        local_evento = evento.local_evento
        capacidade = evento.capacidade
        valor_ingresso = evento.valor_ingresso
        responsavel = evento.responsavel
        status = evento.status

        # cria o cursor, objeto responsável por executar as queries SQL e lê os resultados
        cursor = conn.cursor()
        # a linha 42-43 é a query SQL que será executada, tudo que tem um : na frente é um placeholder que será substituído pelo valor da variável correspondente
        sql = """insert into EVENTOS (id_evento, nome_evento, categoria, data_evento, local_evento, capacidade, valor_ingresso, responsavel, status) 
        values (:id_evento, :nome_evento, :categoria, :data_evento, :local_evento, :capacidade, :valor_ingresso, :responsavel, :status)"""

        # tenta executar, caso não consiga, faz rollback (rollback desfaz transações não confirmadas) e exibe mensagem de erro
        try:
            # executa o INSERT, ligando cada bind variavel pelo seu valor (os binds foram definidos em :id_evento, :nome_evento, etc na linha 42-43)
            cursor.execute(
                sql,
                id_evento=id_evento,
                nome_evento=nome_evento,
                categoria=categoria,
                data_evento=data_evento,
                local_evento=local_evento,
                capacidade=capacidade,
                valor_ingresso=valor_ingresso,
                responsavel=responsavel,
                status=status,
            )
            # commit: confirma a transação e grava o resultado no banco de dados, sem isso, o INSERT não é efetivado
            conn.commit()
            print("Cadastro realizado com sucesso!")

        # pega o erro caso aconteça algum problema na execução do INSERT    
        except oracledb.Error as erro:
            conn.rollback()
            print("\nFalha ao cadastrar no banco:", erro)

        # finally: roda sempre, independente de ter dado erro ou não, fecha o cursor e a conexão com o banco de dados
        finally:
            cursor.close()
            conn.close()

    def listar_eventos(self):
        conn = self.conexao.conectar()
        if conn is None:
            print("Erro ao conectar ao Oracle.")
            return False

        cursor = conn.cursor()
        sql = """select id_evento, nome_evento, categoria, data_evento, local_evento, capacidade, valor_ingresso, responsavel, status, data_cadastro 
            from eventos order by id_evento"""

        try:
            cursor.execute(sql)
            eventos = cursor.fetchall()
            if len(eventos) == 0:
                return []
            else:
                return eventos

        except oracledb.Error as erro:
            print("Houve um erro: ", erro)
            eventos = []

        finally:
            cursor.close()
            conn.close()

    def buscar_id_evento(self, id_evento):
        conn = self.conexao.conectar()
        if conn is None:
            return "Erro ao conectar ao Oracle."

        cursor = conn.cursor()
        sql = """select id_evento, nome_evento, categoria, data_evento, local_evento,
                 capacidade, valor_ingresso, responsavel, status, data_cadastro
                 from eventos
                 where id_evento = :id_evento"""

        try:
            cursor.execute(sql, id_evento=id_evento)
            evento = cursor.fetchone()
            if evento is None:
                return None
            else:
                return evento

        except oracledb.Error as erro:
            print("Houve um erro: ", erro)
            return None

        finally:
            cursor.close()
            conn.close()

    def editar_evento(self, evento):
        conn = self.conexao.conectar()
        if conn is None:
            print("Erro ao conectar ao Oracle.")
            return False

        cursor = conn.cursor()
        sql = """update eventos
                 set nome_evento = :nome_evento,
                     categoria = :categoria,
                     data_evento = :data_evento,
                     local_evento = :local_evento,
                     capacidade = :capacidade,
                     valor_ingresso = :valor_ingresso,
                     responsavel = :responsavel,
                     status = :status
                 where id_evento = :id_evento"""

        try:
            cursor.execute(
                sql,
                nome_evento=evento.nome_evento,
                categoria=evento.categoria,
                data_evento=evento.data_evento,
                local_evento=evento.local_evento,
                capacidade=evento.capacidade,
                valor_ingresso=evento.valor_ingresso,
                responsavel=evento.responsavel,
                status=evento.status,
                id_evento=evento.id_evento,
            )

            if cursor.rowcount == 0:
                conn.rollback()
                return None

            conn.commit()
            return True

        except oracledb.Error as erro:
            conn.rollback()
            print("\nFalha ao editar no banco:", erro)
            return False

        finally:
            cursor.close()
            conn.close()

    def excluir_evento(self, id_evento):
        conn = self.conexao.conectar()
        if conn is None:
            print("Erro ao conectar ao Oracle.")
            return False

        cursor = conn.cursor()
        sql = "delete from eventos where id_evento = :id_evento"

        try:
            cursor.execute(sql, id_evento=id_evento)

            if cursor.rowcount == 0:
                conn.rollback()
                return None

            conn.commit()
            return True

        except oracledb.Error as erro:
            conn.rollback()
            print("\nFalha ao excluir no banco:", erro)
            return False

        finally:
            cursor.close()
            conn.close()
