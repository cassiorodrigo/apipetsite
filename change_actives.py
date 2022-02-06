import sqlite3


class Conectar:
    def __init__(self):
        self.conn = None
        self.c = None

    def __enter__(self):
        self.conn = sqlite3.connect('dados/administracao.db')
        self.c = self.conn.cursor()
        return self

    def __exit__(self, *args):
        return args

    def get_nomes(self):
        nomes = list()
        q = "SELECT NOME_CAO FROM inscricoes WHERE(DIAS_POR_SEMANA NOT LIKE '%otel%') ORDER BY NOME_CAO"
        res = self.c.execute(q).fetchall()
        nomes = [nome[0] for nome in res]
        return nomes

    def set_inativos(self):
        lista_todos = ['Alfredo ', 'Amora', 'Balu', 'Billy Jack', 'Faísca ', 'Gaia', 'Lolla', 'Marcelino',
                       'Nome do Cão', 'Pipoca','Theo Golden (Theodoro)', 'Thielo Sabino']
        for e in lista_todos:
            q = f"UPDATE inscricoes SET ATIVO=0 WHERE(NOME_CAO like '%{e}')"
            self.c.execute(q)
            self.conn.commit()
        res = self.c.execute("SELECT NOME_CAO FROM inscricoes WHERE(DIAS_POR_SEMANA NOT LIKE '%otel%') ORDER BY NOME_CAO")
        return res

    def set_ativos(self, nome, state):
        dados = state, nome
        query = """
        UPDATE inscricoes SET ATIVO=? WHERE(NOME_CAO like ?)
        """
        self.c.execute(query, dados)
        self.conn.commit()

    def get_dog_details(self, nome):
        dados = nome, 1
        query = """
                SELECT * FROM inscricoes WHERE(NOME_CAO like ? AND ATIVO=?)
                """
        res = self.c.execute(query, dados).fetchone()
        return res


class Banhos(Conectar):
    def __init__(self):
        super().__enter__()
        self.banhos = None

    def get_all_banhos(self):
        q = """
        SELECT * FROM banhos;
        """
        res = self.c.execute(q).fetchall()
        return res


class Fatura(Conectar):
    def __init__(self, nomecao):  # nometutor, dias_por_semana, consumo, dias_hotel, valor_diferenciado=None
        super().__enter__()
        dados = self.get_dog_details(nomecao)
        tutor, email, cao, dias_por_semana, ativo = dados[1], dados[2], dados[4], dados[6], dados[-1]

        fatura = f"""
Olá, {tutor.title.strip()}!

    A Pet Fatura de {cao.title.strip()} chegou!
"""
        valores = {
            1: 200,
            2: 300,
            3: 400,
            4: 500,
            5: 600,
            6: 650}
        # if not valor_diferenciado:
        #     self.valor = valores[dias_por_semana]


if __name__ == "__main__":
    with Fatura('Céu') as fat:
        pass
    # with Conectar() as ncon:
    #     print(ncon.set_ativos('Gaia', 1))