import sqlite3
import pandas as pd


class GoogleDB:
    def __init__(self):
        self.q = None
        self.conn = None
        self.c = None

    def createdb(self):
        self.q = """
        CREATE TABLE IF NOT EXISTS formsinsc(
        _ID INTEGER PRIMARY KEY,
        nome TEXT, 
        telefone INTEGER, 
        email TEXT, 
        nascimento_dono INTEGER, 
        endereco TEXT, 
        dias_por_semana INTEGER, 
        nascimento_cao INTEGER,
        checkin INTEGER, 
        checkout INTEGER, 
        vacinas TEXT, 
        diretrizes TEXT, 
        aceite TEXT, 
        historico_agressividade TEXT,
        clinicavet TEXT, 
        telclinicavet INT, 
        ativo INT DEFAULT 1,
        public_id TEXT
        )
        """
        self.c.execute(self.q)
        self.conn.commit()
        return self.q

    def __enter__(self):
        self.conn = sqlite3.connect('dados/googleinsc.db')
        self.c = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()
        print(exc_tb)
        print(exc_val)
        print(exc_type)
        return exc_val


class InscricaoFromGoogle:
    def __init__(self, lista_respostas:list):
        self.resposta = lista_respostas
        colunas = ["nome", "telefone", "email", "nascimento_dono", "endereco", "dias_por_semana", "nascimento_cao",
                   "checkin", "checkout", "vacinas", "diretrizes", "aceite", "historico_agressividade", "clinicavet",
                   "telclinicavet", "ativo", "public_id"]

        self.to_insert = dict(zip(colunas, self.resposta))

    def create_statement(self):
        pass

    def insert(self):
        try:
            with GoogleDB() as gdb:
                gdb.c.execute(
                    """
                    INSERT INTO formsinsc(
                    nome,
                    telefone,
                    email,
                    nascimento_dono,
                    endereco,
                    dias_por_semana,
                    nascimento_cao,
                    checkin,
                    checkout,
                    vacinas,
                    diretrizes,
                    aceite,
                    historico_agressividade,
                    clinicavet,
                    telclinicavet
                    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                    """, self.resposta)
                return True
        except Exception as err:
            print(err)
            return False

    def monta_fatura(self):
        with open('templatetextos/basefaturas.txt', 'r', encoding='UTF-8') as file:
            base = file.read()
            print(self.resposta)
            fatura = base.format(*self.resposta)
            return fatura


class StraightFromGoogle:
    def __init__(self):
        self.conn = sqlite3.connect('dados/fromgoogle.db')
        self.c = self.conn.cursor()

    def __enter__(self):
        self.conn = sqlite3.connect('dados/fromgoogle.db')
        self.c = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()

    def registrar(self, datafromgoogle):
        try:
            df = pd.DataFrame(datafromgoogle, index=["",])
            df.to_sql("inscricoes", con=self.conn, if_exists='replace')
            return True
        except ValueError as err:
            print("Value error!")
            print(err)
            return False


class Reservas:
    pass


class Banho:
    pass


if __name__ == "__main__":
    with GoogleDB() as gdb:
        gdb.createdb()
