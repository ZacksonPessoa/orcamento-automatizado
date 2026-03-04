"""
Conexão com o banco Firebird (Fcerta) e consulta à tabela fc03000.
Configuração via variáveis de ambiente (FIREBIRD_*).
"""
import os
from typing import Any

# Configuração padrão; pode ser sobrescrita por .env
HOST = os.getenv("FIREBIRD_HOST", "192.168.5.160")
CAMINHO_BANCO = os.getenv("FIREBIRD_DATABASE", r"D:\Fcerta\DB\ALTERDB.ib")
USUARIO = os.getenv("FIREBIRD_USER", "SYSDBA")
SENHA = os.getenv("FIREBIRD_PASSWORD", "masterkey")
CHARSET = os.getenv("FIREBIRD_CHARSET", "WIN1252")


def get_connection():
    """Abre e retorna uma conexão com o Firebird."""
    import fdb
    return fdb.connect(
        host=HOST,
        database=CAMINHO_BANCO,
        user=USUARIO,
        password=SENHA,
        charset=CHARSET,
    )


def query_fc03000(limite: int | None = None) -> list[dict[str, Any]]:
    """
    Consulta a tabela fc03000 e retorna:
    DESCR (descrição), UNID (unidade cadastrada), UNIRC (unidade receita),
    PROCMN (preço de compra), PRVEN (preço de venda).
    """
    con = get_connection()
    try:
        cur = con.cursor()
        sql = "SELECT DESCR, UNID, UNIRC, PROCMN, PRVEN FROM fc03000"
        if limite is not None:
            sql = f"SELECT FIRST {int(limite)} DESCR, UNID, UNIRC, PROCMN, PRVEN FROM fc03000"
        cur.execute(sql)
        colunas = ["DESCR", "UNID", "UNIRC", "PROCMN", "PRVEN"]
        rows = cur.fetchall()
        cur.close()
        return [
            dict(zip(colunas, row))
            for row in rows
        ]
    finally:
        con.close()


def query_fc03000_por_descricao(descricao: str, limite: int = 50) -> list[dict[str, Any]]:
    """
    Busca na fc03000 por descrição (DESCR) contendo o texto informado.
    Retorna os mesmos campos: DESCR, UNID, UNIRC, PROCMN, PRVEN.
    """
    con = get_connection()
    try:
        cur = con.cursor()
        # CONTAINING no Firebird é case-insensitive
        cur.execute(
            f"SELECT FIRST {int(limite)} DESCR, UNID, UNIRC, PROCMN, PRVEN FROM fc03000 "
            "WHERE DESCR CONTAINING ?",
            (descricao.strip(),),
        )
        colunas = ["DESCR", "UNID", "UNIRC", "PROCMN", "PRVEN"]
        rows = cur.fetchall()
        cur.close()
        return [dict(zip(colunas, row)) for row in rows]
    finally:
        con.close()
