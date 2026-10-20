import oracledb
from connOracle.conndb import Conexaodb

def obter_conexao():
    conexao = Conexaodb(
        usuario="rm573234",
        senha="110408",
        host="oracle.fiap.com.br",
        porta="1521",
        service_name="ORCL"
    );
    return conexao_obj.conectar():

def inserir_evento(evento):
    conexao = Nonecursor = None
    try:
        conexao = obter_conexao()
        cursor = conexao.cursor()
        sql = """INSERT INTO EVENTOS (id_evento, nome_evento, categoria, data_evento, local_evento, capacidade, valor_ingresso, responsavel, status)
                 VALUES (:id_evento, :nome_evento, :categoria, :data_evento, :local_evento, :capacidade, :valor_ingresso, :responsavel, :status)"""
        cursor.execute(sql, evento.to_dict())
        conexao.commit()
        return True
    except oracledb.Error as erro:
        if conexao:
            conexao.rollback()
        print("Erro ao inserir evento:", erro)
        return False
    finally: 
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()