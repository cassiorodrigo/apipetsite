import sqlite3
import pandas as pd
from monta_fatura import assign_public_id


class Conexao:

    def __init__(self):
        self.conn = None
        self.c = None

    def __enter__(self):
        self.conn = sqlite3.connect('dados/administracao.db')
        self.c = self.conn.cursor()
        return self

    def __exit__(self, *args):
        self.conn.commit()
        return print('exited')


class InscreverDog:

    def __init__(self, **kwargs):
        self.colunas = list()
        self.values = list()
        kwargs['protocolos'] = ''.join([kwargs.get('vacinado'),kwargs.get('vermifugado'), kwargs.get('castrado')])
        toremove = ["vacinado", "vermifugado", "castrado", "submit"]
        try:
            for e in toremove:
                kwargs.pop(e)
        except KeyError:
            pass

        self.forms = kwargs
        print(f"[FROM INSCRICOES] kwargs formatado transformado em dict: \n{self.forms}")
        if self.forms.get('crechehotel') == 'Creche':
            self.forms.setdefault('ativo', 1)
        else:
            self.forms.setdefault('ativo', 0)

    def inscrever_dog(self):
        colunas = list(self.forms.keys())
        valores = list(self.forms.values())
        print(colunas)
        print(valores)
        q = f"""
        insert into inscricoes(
        {','.join(colunas)}
        ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """
        with Conexao() as conn:
            conn.c.execute(q, valores)
            conn.conn.commit()
        assign_public_id()
