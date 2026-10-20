from connOracle.conndb import Conexaodb
import oracledb

class EventoDAO:
    def __init__(self):
        self.conexao = Conexaodb(
            usuario="rm569961",
            senha="030308",
            host="host",
            porta=1521,
            service_name="ORCL"
        )

    def cadastrar_evento(self, evento):
        conn = self.conexao.conectar()
        if conn is None:
            print("Erro ao conectar ao Oracle.")
            return False

        id_evento = evento.id_evento
        nome_evento = evento.nome_evento
        categoria = evento.categoria
        data_evento = evento.data_evento
        local_evento = evento.local_evento
        capacidade = evento.capacidade
        valor_ingresso = evento.valor_ingresso
        responsavel = evento.responsavel
        status = evento.status        

        cursor = conn.cursor()
        sql = """insert into EVENTOS (id_evento, nome_evento, categoria, data_evento, local_evento, capacidade, valor_ingresso, responsavel, status) 
        values (:id_evento, :nome_evento, :categoria, :data_evento, :local_evento, :capacidade, :valor_ingresso, :responsavel, :status)"""

        try:
            cursor.execute(sql,
                           id_evento = id_evento,
                           nome_evento = nome_evento,
                           categoria = categoria, 
                           data_evento = data_evento,
                           local_evento = local_evento,
                           capacidade = capacidade,
                           valor_ingresso = valor_ingresso,
                           responsavel = responsavel,
                           status = status
                           )
            conn.commit()
            print("Cadastro realizado com sucesso!")

        except oracledb.Error as erro:
            conn.rollback()
            print("\nFalha ao cadastrar no banco:", erro)
    
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
                    return None
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
            print("Erro ao conectar ao Oracle.")
            return False

        cursor = conn.cursor()
        sql = """select id_evento, nome_evento, categoria, data_evento, local_evento,
                 capacidade, valor_ingresso, responsavel, status, data_cadastro
                 from eventos
                 where id_evento = :id_evento"""

        try:
            cursor.execute(sql, id_evento=id_evento)
            evento = cursor.fetchone()
            if evento == None:
                return None
            else:
                return None  

        except oracledb.Error as erro:
            print("Houve um erro: ", erro)

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
            cursor.execute(sql,
                           nome_evento=evento.nome_evento,
                           categoria=evento.categoria,
                           data_evento=evento.data_evento,
                           local_evento=evento.local_evento,
                           capacidade=evento.capacidade,
                           valor_ingresso=evento.valor_ingresso,
                           responsavel=evento.responsavel,
                           status=evento.status,
                           id_evento=evento.id_evento)

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