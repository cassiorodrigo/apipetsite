import calendar
import sqlite3
import uuid
from databasehandler import FaturasDB, DatabaseCaes
from calendar import month_abbr, different_locale
from datetime import date
mes = calendar.month_abbr[date.today().month]
ano = date.today().year
tabela_do_mes = f'{mes}{ano}'

def monta_fatura(token):
    with FaturasDB() as fat:
        with open('templatetextos/basefaturas.txt', 'r') as file:
            base_fatura = file.read()
            dog = fat.get_fatura(token)
            print(base_fatura.format(*dog))



def create_fatura():
    pass


def assign_public_id():
    with sqlite3.connect('dados/administracao.db') as dbdog:
        c = dbdog.cursor()
        pid = c.execute('select PUBLIC_ID from inscricoes').fetchone()
        insert = '''
        UPDATE inscricoes SET PUBLIC_ID=? where PUBLIC_ID is NULL
        '''

        public_id = uuid.uuid4().hex
        while pid[0] == public_id:
            public_id = uuid.uuid4().hex

        c.execute(insert, [public_id,])
        dbdog.commit()


def assign_token():
    with FaturasDB() as fat:
        fat.set_token()


def link_pid_informacoes():
    with DatabaseCaes() as dbc:
        pids = f"""
        SELECT public_id, NOME_CAO FROM inscricoes
        """
        update = f'''
        UPDATE {tabela_do_mes} SET PUBLIC_ID=? WHERE dog=?
        '''
        listaexecucoes = list()
        dbc.c.execute(pids)
        for e in dbc.c:
            listaexecucoes.append(e)

        try:
            dbc.c.executemany(update, listaexecucoes)
        except Exception as err:
            print(err)
        finally:
            dbc.conn.commit()

def link_pid_faturas():
    with DatabaseCaes() as dbc:
        pids = """
        SELECT public_id, NOME_CAO FROM inscricoes
        """
        update = '''
        UPDATE faturas SET PUBLIC_ID=? WHERE NOMECAO=?
        '''
        listaexecucoes = list()
        dbc.c.execute(pids)
        for e in dbc.c:
            listaexecucoes.append(e)

        try:
            dbc.c.executemany(update, listaexecucoes)
        except Exception as err:
            print(err)
        finally:
            dbc.conn.commit()


if __name__ == "__main__":
    # assign_public_id()
    monta_fatura(token='eb3be7e5dcb0485bba002d08c6a66e71')
    # assign_token()
    # print(assign_public_id())
    # resultado = get_data_from_db("f0e8e5e0027e465e931d0d72b750b47d")
    # print(resultado)