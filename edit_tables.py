import sqlite3


class Connection:
    def __init__(self):
        self.conn = None
        self.c = None

    def __enter__(self):
        self.conn = sqlite3.connect('dados/administracao.db')
        self.c = self.conn.cursor()
        return self

    def __exit__(self, *args):
        return args

    def get_nome_tabelas(self):
        q = """
        SElECT NAME FROM sqlite_master WHERE NAME NOT LIKE 'sqlite_%' AND
        NAME NOT LIKE '%_index'
        """
        return self.c.execute(q)

    def get_table_columns(self, tabela):
        tabelas = self.get_nome_tabelas()
        for e in tabelas:
            if tabela == e[0]:
                result = self.c.execute(f"PRAGMA table_info({tabela})").fetchall()
                return result
        return 'Tabela não achada'

    def select_tudo_from_table(self, tabela):
        todas_tabelas = self.get_nome_tabelas()
        for e in todas_tabelas:
            if e[0] == tabela:
                q = """
                SELECT * FROM {}
                """.format(tabela)
                return self.c.execute(q)

        return 'Tabela não encontrada'

    def get_all_info(self):
        tabelas = self.get_nome_tabelas().fetchall()
        dados = dict()
        for tabela in tabelas:
            colunas = list()
            q =f"""
            PRAGMA table_info({tabela[0]})
            """
            cols = self.c.execute(q).fetchall()
            for resultado in cols:
                colunas.append(resultado)
            dados[tabela[0]] = colunas
        return dados


if __name__ == "__main__":
    with Connection() as conn:
        dados = conn.get_all_info()
        print(dados)


        # res = conn.get_table_columns('banhos')
        # for e in res:
        #     print(e)

