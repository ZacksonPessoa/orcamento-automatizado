"""
Conexão com o banco Firebird (Fcerta) e consulta à tabela fc03000.
Configuração via variáveis de ambiente (FIREBIRD_*).
"""
import os
from decimal import Decimal
from typing import Any


def _to_jsonable(v: Any) -> Any:
    """Converte Decimal e outros tipos não serializáveis em JSON para número/string."""
    if isinstance(v, Decimal):
        return float(v)  # ou str(v) se quiser precisão exata
    return v

# Configuração padrão; pode ser sobrescrita por .env
HOST = os.getenv("FIREBIRD_HOST", "192.168.5.160")
CAMINHO_BANCO = os.getenv("FIREBIRD_DATABASE", r"D:\Fcerta\DB\ALTERDB.ib")
USUARIO = os.getenv("FIREBIRD_USER", "SYSDBA")
SENHA = os.getenv("FIREBIRD_PASSWORD", "masterkey")
CHARSET = os.getenv("FIREBIRD_CHARSET", "WIN1252")

# Colunas de preço na fc03000 (ajuste se no seu banco tiver outros nomes)
COL_PRECO_COMPRA = os.getenv("FIREBIRD_COL_PRECO_COMPRA", "PRCOMN")
COL_PRECO_VENDA = os.getenv("FIREBIRD_COL_PRECO_VENDA", "PRVEN")


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


def _campos_preco():
    """Lista de campos de preço para SELECT (pode vir de colunas com outros nomes no banco)."""
    return [COL_PRECO_COMPRA, COL_PRECO_VENDA]


def query_fc03000(limite: int | None = None) -> list[dict[str, Any]]:
    """
    Consulta a tabela fc03000 e retorna:
    DESCR (descrição), UNIDA (unidade cadastrada), UNIRC (unidade receita),
    preço de compra, preço de venda (nomes das colunas configuráveis por FIREBIRD_COL_*).
    """
    campos = ["DESCR", "UNIDA", "UNIRC"] + _campos_preco()
    con = get_connection()
    try:
        cur = con.cursor()
        sel = ", ".join(campos)
        sql = f"SELECT {sel} FROM fc03000"
        if limite is not None:
            sql = f"SELECT FIRST {int(limite)} {sel} FROM fc03000"
        cur.execute(sql)
        desc = cur.description
        rows = cur.fetchall()
        cur.close()
        return [
            {desc[i][0].strip(): _to_jsonable(row[i]) for i in range(len(desc))}
            for row in rows
        ]
    finally:
        con.close()


def query_fc03000_por_descricao(descricao: str, limite: int = 50) -> list[dict[str, Any]]:
    """
    Busca na fc03000 por descrição (DESCR) contendo o texto informado.
    Retorna os mesmos campos: DESCR, UNIDA, UNIRC, PROCMN, PRVEN.
    """
    campos = ["DESCR", "UNIDA", "UNIRC"] + _campos_preco()
    sel = ", ".join(campos)
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute(
            f"SELECT FIRST {int(limite)} {sel} FROM fc03000 WHERE DESCR CONTAINING ?",
            (descricao.strip(),),
        )
        desc = cur.description
        rows = cur.fetchall()
        cur.close()
        return [
            {desc[i][0].strip(): _to_jsonable(row[i]) for i in range(len(desc))}
            for row in rows
        ]
    finally:
        con.close()
