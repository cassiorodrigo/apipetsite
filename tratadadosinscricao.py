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
    """
    {'nome': 'Cassio Rodrigo DAntonio Peluso', 'dog': 'Cassio Rodrigo DAntonio Peluso', 'raca': 'Labrador', 'email': 'cassiorodrigo@gmail.com', 'telefone': '911077096', 'endereco': 'Av. Alexandre Herculano', 'diretrizes': 'nao', 'vacinado': 'y', 'vermifugado': 'y', 'castrado': 'y', 'crechehotel': 'Hotel', 'dataadaptacao': '2022-02-12', 'checkin': '2022-02-13', 'checkout': '2022-02-15', 'dias_por_semana': '1', 'nascimento_cao': '2021-12-08', 'historico_agressividade': 'fa', 'clinicavet': 'veterinario', 'telclinicavet': '+351911077096', 'submit': 'Enviar'}
    """

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
        for colunas, valores in kwargs.items():
            self.colunas.append(colunas)
            self.values.append(valores)
        self.values.append('1')

    def createdf(self):
        return pd.DataFrame([self.forms])



    def inscrever_dog(self):
        colunas = ','.join(list(self.createdf().columns))
        print(f"[FROM INSCREVER DOGS LINHA 48] colunas E colunas len: {colunas}\n{len(colunas)}")
        valores = self.createdf().values.tolist()
        print(f"[FROM INSCREVER DOGS LINHA 50] valores E valores len: {valores[0]}\n{len(valores[0])}")
        # colunas = ['NOME_CAO', 'TUTOR', 'RACA', 'EMAIL', 'TEL_TUTOR', 'ENDERECO', 'CUIDADOS_ESPECIAIS', 'TIPO_CADASTRO', 'ADAPTACAO', 'CHECKIN', 'CHECKOUT', 'DIAS_POR_SEMANA', 'NASCIMENTO_CAO', 'AGRESSIVIDADE', 'VET', 'TEL_VET', 'PROTOCOLOS', 'ATIVO', 'public_id']
        q = f"""
        insert into inscricoes(
        {colunas}
        ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """
        with Conexao() as conn:
            conn.c.execute(q, valores[0])
            conn.conn.commit()
        assign_public_id()


# if __name__ == "__main__":
#     Inscricao.inscrever_dog()