import pandas as pd
from databasehandler import FaturasDB
from datetime import datetime
import calendar
import locale


def iniciar_tabela_faturas():
    locale.setlocale(locale.LC_ALL, 'pt_br')
    nome_tabela = calendar.month_abbr[datetime.now().month]+str(datetime.now().year)
    df = pd.read_csv('dados/dados.csv')
    schema = """
    PUBLIC_ID TEXT,
    TUTOR TEXT,
    DOG TEXT,
    TAMANHO INTEGER,
    TELEFONE TEXT,
    VALORCRECHE REAL,
    DIASPORSEMANA INTEGER,
    MEIOPERIODO INTEGER,
    TAMANHO INTEGER,
    DIASHOTEL INTEGER,
    DATABANHO INTEGER,
    QUANTIDADEBANHOS INTEGER,
    TOTALBANHOS REAL,
    CONSUMO TEXT,
    VALORCONSUMO REAL,
    TOKEN TEXT
    """
    with FaturasDB() as fat:
        df.to_sql(nome_tabela, fat.conn, schema=schema)


if __name__ == "__main__":
    iniciar_tabela_faturas()