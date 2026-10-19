def inserir_evento(evento):
    conexao = None
    cursor = None
    try:
        conexao = obter_conexao()
        cursor = conexao.cursor()
        sql = """INSERT INTO EVENTOS (
                    ID_EVENTO, NOME_EVENTO, CATEGORIA, DATA_EVENTO,
                    LOCAL_EVENTO, CAPACIDADE, VALOR_INGRESSO,
                    RESPONSAVEL, STATUS
                ) VALUES (
                    :id_evento, :nome_evento, :categoria, :data_evento,
                    :local_evento, :capacidade, :valor_ingresso,
                    :responsavel, :status
                )"""
        cursor.execute(sql, evento.to_dict())
        conexao.commit()
        return True
    except oracledb.DatabaseError as e:
        # tratar erro específico
        if conexao: conexao.rollback()
        return False
    finally:
        if cursor: cursor.close()
        if conexao: conexao.close()