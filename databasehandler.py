import calendar
import sqlite3
from flask_bcrypt import generate_password_hash, check_password_hash
from datetime import datetime
import uuid
from calendar import month_abbr, different_locale


class ConectDb:
    def __init__(self):
        self.conn = None
        self.c = None

    def __enter__(self):
        self.conn = sqlite3.connect('dados/administracao.db')
        self.c = self.conn.cursor()
        return self

    def __exit__(self, *args):
        if args[0]:
            print(f"Exited with args: {args}")
        self.conn.close()


class ClockRecorder(ConectDb):
    def __init__(self):
        super().__enter__()
        create = """
        CREATE TABLE IF NOT EXISTS clock(
        _ID INTEGER PRIMARY KEY AUTOINCREMENT,
        USERNAME TEXT,
        EMAIL TEXT, 
        CLOCKIN REAL DEFAULT NULL,
        CLOCKOUT REAL DEFAULT NULL,
        DELTA REAL,
        UNIQUE(USERNAME, CLOCKIN, CLOCKOUT)
        )
        """
        self.c.execute(create)
        self.conn.commit()

    def insert_clockin(self, username, email):
        tudo = self.c.execute("SELECT COUNT(*) FROM clock").fetchone()[0]
        # print(tudo)
        tstamp = datetime.timestamp(datetime.now())
        if tudo == 0:
            self.c.execute("INSERT INTO clock(USERNAME, EMAIL, CLOCKIN) VALUES(?,?,?)",[username, email, tstamp])
        else:
            last_login_id = self.c.execute("SELECT MAX(_ID) FROM clock WHERE(USERNAME=?)", [username,]).fetchone()[0]
            # print(f"LASTLOGIN_ID: {last_login_id}")
            if last_login_id is None:
                # print('last login id is none')
                self.c.execute("INSERT INTO clock(USERNAME, EMAIL, CLOCKIN) VALUES(?,?,?)", [username, email, tstamp])
                self.conn.commit()
                return True
            last_login = self.c.execute("SELECT * FROM clock WHERE(_ID=?)", [last_login_id,]).fetchone()
            # print(f"[LASTLOGIN] {last_login}")
            if last_login[3] is not None and last_login[4] is None:
                self.insert_clockout(last_login_id)
            elif last_login[3] is not None and last_login[4] is not None:
                self.c.execute("INSERT INTO clock(USERNAME, EMAIL, CLOCKIN) VALUES(?,?,?)",
                               [username, email, tstamp])
        self.conn.commit()

    def insert_clockout(self, identity):
        clockouttime = datetime.timestamp(datetime.now())
        clockintime = self.c.execute("SELECT CLOCKIN FROM clock WHERE (_ID=?)", [identity,]).fetchone()[0]
        deltat = clockouttime - clockintime
        dados = [clockouttime, deltat, identity]
        insert = """
               UPDATE clock SET CLOCKOUT=?, DELTA=? WHERE(_ID=?)
               """
        self.c.execute(insert, dados)
        self.conn.commit()

    def is_clocked_in(self, email):
        clocked = """
        SELECT MAX(_ID) FROM clock WHERE(EMAIL=? AND CLOCKOUT IS NULL)
        """
        last_clockin = self.c.execute(clocked, [email,]).fetchone()[0]
        if last_clockin is not None:
            return True
        return False

    def is_clocked_out(self, email):
        clocked = """
                SELECT MAX(_ID) FROM clock WHERE(EMAIL=? AND CLOCKOUT IS NOT NULL)
                """
        last_clockout = self.c.execute(clocked, [email, ]).fetchone()[0]
        if last_clockout is not None:
            return True
        return False

    def prestador_state(self, email):
        try:
            clocked = """
                    SELECT MAX(_ID) FROM clock WHERE(EMAIL=?)
                    """
            last_entry = self.c.execute(clocked, [email, ]).fetchone()[0]
            clockedinout = self.c.execute("SELECT CLOCKIN, CLOCKOUT FROM clock WHERE(_ID=?)", [last_entry,]).fetchone()
            # print(clockedinout)
            if clockedinout[0] is not None and clockedinout[1] is None:
                return True  # True is logged FALSE is not logged
            return False
        except TypeError as Terror:
            return False

    def get_clockin_time(self, email):
        q = "SELECT CLOCKIN FROM clock WHERE EMAIL=? ORDER BY _ID DESC LIMIT 1"
        res = self.c.execute(q, [email,]).fetchone()
        return res


class Posts(ConectDb):
    def __init__(self):
        super().__enter__()
        create = """
        CREATE TABLE IF NOT EXISTS posts(
        _ID INTEGER PRIMARY KEY AUTOINCREMENT,
        AUTHOR TEXT,
        POST TEXT,
        IMAGE_LINK TEXT,
        TIMESTAMP TEXT DEFAULT DATETIME('now')
        )
        """
        self.c.execute(create)
        self.conn.commit()


class Banhos(ConectDb):
    def __init__(self):
        super().__enter__()
        # self.conn = sqlite3.connect("dados/administracao.db")
        # self.c = self.conn.cursor()

        create = """
        CREATE TABLE IF NOT EXISTS banhos(
        _ID INTEGER PRIMARY KEY AUTOINCREMENT,
        NOMECAO TEXT,
        DATAPEDIDO TEXT,
        DATABANHO TEXT,
        TAMANHOCAO TEXT,
        BANHO_DADO INTEGER DEFAULT 0,
        UNIQUE(NOMECAO, DATABANHO)
        )
        """
        self.c.execute(create)
        self.conn.commit()

    def inserir_banho(self, nome, data_pedido, data_banho, tamanho_cao='medio'):

        query = """
        INSERT INTO banhos(NOMECAO, DATAPEDIDO, DATABANHO, TAMANHOCAO) values(?, ?, ?, ?)
        """
        self.c.execute(query, [nome, data_pedido, data_banho, tamanho_cao])
        self.conn.commit()

    def deletar_banho(self, nome, data):
        query = """
        DELETE FROM banhos WHERE(NOMECAO==:nomecao AND DATABANHO==:databanho)
        """
        self.c.execute(query, {"nomecao": nome, "databanho": data})
        self.conn.commit()

    def mostrar_banhos(self):
        query = """
        SELECT NOMECAO, date(DATAPEDIDO, 'unixepoch'), 
        date(DATABANHO, 'unixepoch')
        FROM banhos WHERE(DATABANHO >=  strftime('%s', datetime('now')) AND BANHO_DADO IS NOT NULL)
        """
        res = self.c.execute(query).fetchall()
        return res

    def update_banho_tomado(self, nome, data_banho, banho_tomado: bool):

        dados = banho_tomado, nome, data_banho
        update = """
        UPDATE banhos SET BANHO_DADO=? WHERE(NOMECAO=? AND DATABANHO=?)
        """
        self.c.execute(update, dados)
        self.conn.commit()

    def mostrar_banhos_ultimo_mes(self):
        pass


class Chegadas(ConectDb):
    def __init__(self):
        super().__enter__()
        # self.conn = sqlite3.connect('dados/administracao.db')
        # self.c = self.conn.cursor()
        create = """
        CREATE TABLE IF NOT EXISTS chegadas(
        _ID INTEGER PRIMARY KEY AUTOINCREMENT,
        NOMECAO TEXT,
        DATACHEGADA TEXT,
        DATASAIDA TEXT,
        ADAPTACAO TEXT,
        UNIQUE(NOMECAO, DATACHEGADA)
        )
        """
        create_adaptacao = """
        CREATE TABLE IF NOT EXISTS adaptacao(
        _ID INTEGER PRIMARY KEY AUTOINCREMENT,
        TUTOR TEXT,
        DOG TEXT,
        DATACHEGADA TEXT,
        RACA TEXT,
        TELEFONE TEXT,
        EMAIL TEXT,
        DIRETRIZES TEXT,
        CRECHEHOTEL INTEGER,
        UNIQUE(DOG, DATACHEGADA)
        )
        """
        self.c.execute(create)
        self.c.execute(create_adaptacao)
        self.conn.commit()

    def insert_adaptacao(self, **kwargs):

        """
        :param kwargs:
        tutor, dog, datachegada, raca, telefone, email
        :return:
        """
        print(f'FROM INSERT ADAPTACAO {list(kwargs.values())}')
        q = '''
        INSERT INTO adaptacao(TUTOR, DOG, DATACHEGADA, RACA, TELEFONE, EMAIL, DIRETRIZES,CRECHEHOTEL) VALUES (?,?,?,?,?,?,?,?)
        '''
        self.c.execute(q, list(kwargs.values())[0])
        self.conn.commit()

    def insert_new_arrival(self, nomecao, chegada, saida, adaptacao):
        data = nomecao, chegada, saida, adaptacao

        self.c.execute("""
        INSERT OR IGNORE INTO chegadas(NOMECAO, DATACHEGADA, DATASAIDA, ADAPTACAO) VALUES (?,?,?,?)
        """, data)
        self.conn.commit()

    def get_arrivals_names(self):
        self.c.execute("""
                    Select
                    NOMECAO
                    FROM chegadas
                    WHERE (DATACHEGADA >= strftime('%s','now') OR
                    DATASAIDA >= strftime('%s','now')-3600000)
                    """)

        resultado_busca = self.c.fetchall()
        return resultado_busca

    def check_arrivals(self):
        self.c.execute("""
            Select
            _ID,  
            NOMECAO,
            DATACHEGADA,
            DATASAIDA,
            ADAPTACAO
            FROM chegadas
            WHERE (DATACHEGADA >= strftime('%s','now') OR
            DATASAIDA >= strftime('%s','now')-3600000)
            """)

        resultado_busca = self.c.fetchall()
        print(resultado_busca)
        return resultado_busca

    def delete_arrival(self, nome, chegada):
        self.c.execute("""
        DELETE FROM chegadas WHERE(NOMECAO ==:quecao and DATACHEGADA ==:quedata)
        """, {"quecao": nome, "quedata": chegada})
        self.conn.commit()


class DatabaseUsuarios(ConectDb):
    err = None

    def __init__(self):
        self.dog = None
        super().__enter__()
        # self.conn = sqlite3.connect("dados/administracao.db")
        # self.c = self.conn.cursor()
        self.id = None
        self.public_id = None
        self.nome = None
        self.dog = None
        self.email = None
        self.username = None
        self.role = "cliente"
        create = """
        CREATE TABLE IF NOT EXISTS usuarios(
        _ID INTEGER PRIMARY KEY AUTOINCREMENT,
        PUBLIC_ID TEXT UNIQUE,
        USERNAME TEXT UNIQUE,
        NOMECAO TEXT,
        NOME TEXT UNIQUE,
        EMAIL TEXT UNIQUE,
        ROLE DEFAULT 'cliente',
        UNIQUE(PUBLIC_ID, EMAIL, USERNAME)
        )
        """
        create_senha = """
        CREATE TABLE IF NOT EXISTS segredos(
        _ID INTEGER PRIMARY KEY AUTOINCREMENT,
        SEGREDO_USUARIO TEXT,
        SEGREDO_EMAIL TEXT
        )
        """
        self.c.execute(create)
        self.c.execute(create_senha)
        self.conn.commit()

    def get_user_by_public_id(self, public_id):
        res = self.c.execute("SELECT * FROM usuarios WHERE PUBLIC_ID=?", [public_id, ]).fetchone()
        return res

    def registrar_usuario(self, nome, nomecao, usuario, email, senha):
        try:
            public_id = uuid.uuid4().hex
            publicids = self.c.execute('select PUBLIC_ID FROM usuarios').fetchall()
            for pubid in publicids:
                while public_id in pubid:
                    public_id = uuid.uuid4().hex
            nsenha_usuario = senha+usuario
            nsenha_email = senha+email
            senha_usuario = generate_password_hash(nsenha_usuario)
            senha_email = generate_password_hash(nsenha_email)
            valores = public_id, nome, usuario, email, nomecao
            self.c.execute('''
            INSERT INTO usuarios(PUBLIC_ID, NOME, USERNAME, EMAIL, NOMECAO) VALUES(?,?,?,?,?)
            ''', valores)
            self.c.execute('''
            INSERT INTO segredos(SEGREDO_USUARIO, SEGREDO_EMAIL) VALUES(?,?)
            ''', [senha_usuario, senha_email])
            self.conn.commit()
            return True
        except Exception as err:
            error = str(err).split(".")[1]
            DatabaseUsuarios.err = f"{error} Já cadastrado. Por favor, escolha outro {error}"
            # print(self.err)
            return False

    def login_usuarios(self, usuario, senha) -> bool:

        nsenha = senha+usuario
        if "@" in usuario:
            id_usuario = """
            SELECT _ID from usuarios WHERE(EMAIL=?)
            """
            senha_a_comparar = """
            SELECT SEGREDO_EMAIL FROM segredos WHERE(_ID=?)
            """
        else:
            id_usuario = """
            SELECT _ID from usuarios WHERE(USERNAME=?)
            """
            senha_a_comparar = """
                        SELECT SEGREDO_USUARIO FROM segredos WHERE(_ID=?)
                        """

        getinfo = """
        SELECT * FROM usuarios WHERE(_ID=?)
        """
        ident = self.c.execute(id_usuario, [usuario,]).fetchone()[0]
        self.id, self.public_id, self.username, self.nome, self.dog, self.email, self.role = self.c.execute(getinfo, [ident,]).fetchone()
        s_armazenada = self.c.execute(senha_a_comparar, [ident,]).fetchone()[0]

        return check_password_hash(s_armazenada, nsenha)

    def atualizar_email(self, username):
        pass

    def login_disponivel(self):
        logins = self.c.execute("SELECT USERNAME FROM usuarios").fetchall()
        return logins

    def get_nome_func(self, username):
        self.c.execute('''Select NOME FROM usuarios WHERE (USERNAME = ?)''', [username,])
        resultado = self.c.fetchone()
        return resultado


class DatabaseCaes(ConectDb):
    def __init__(self):
        super().__enter__()
        # self.conn = sqlite3.connect("dados/administracao.db")
        # self.c = self.conn.cursor()

        self.c.execute("""
                CREATE TABLE IF NOT EXISTS inscricoes(
                _ID INTEGER PRIMARY KEY AUTOINCREMENT,
                TUTOR TEXT,
                EMAIL TEXT,
                ENDERECO TEXT,
                NOME_CAO TEXT,
                NASCIMENTO_CAO TEXT,
                DIAS_POR_SEMANA TEXT,
                ENTRADA_HOTEL TEXT,
                SAIDA_HOTEL TEXT,
                VET TEXT,
                TEL_VET TEXT,
                CUIDADOS_ESPECIAIS TEXT,
                RACA TEXT,
                TEL_TUTOR TEXT,
                ATIVO INTEGER,
                UNIQUE(TUTOR, NOME_CAO, RACA)
                )
                """)

    def get_caes(self):
        req = """
        SELECT * FROM inscricoes WHERE (DIAS_POR_SEMANA NOT LIKE '%otel%' AND ATIVO = '1') ORDER BY dog
        """
        res = self.c.execute(req).fetchall()
        return res

    def get_one_dog(self, *args):
        dados = [args[0] for _ in range(4)]

        """
        :param kwargs:
            keys: EMAIL, TUTOR, NOME_CAO, public_id
        :return:
        """
        q = "SELECT * FROM inscricoes WHERE(EMAIL=? or NOME=? or dog=? or public_id=?)"
        try:
            res = list(self.c.execute(q, dados).fetchone())
            return res
        except TypeError:
            return None

    def inserir_inscricoes(self, json_todos_caes) -> bool:
        """
        metodo para ser usado apenas uma vez para criar o DB
        :param json_todos_caes: deve receber um Json com todos os cães vindo, por exemplo, do arquivo parserforscvdata
        :return: Bool para sucesso ou não (TRUE OR FALSE)
        """
        try:
            value = json_todos_caes
            dados = value["tutor"], value["email"], value["endereco"],\
            value["nome_cao"], value["nascimento_cao"], \
            value["dias_por_semana"], \
            value["vet"], value["tel_vet"], value["cuidados_especiais"], value["raca"],\
            value["tel_tutor"], value["ativo"]
            self.conn.execute('''
            INSERT OR IGNORE INTO inscricoes(TUTOR, EMAIL, ENDERECO, NOME_CAO, NASCIMENTO_CAO, DIAS_POR_SEMANA, ENTRADA_HOTEL,
            SAIDA_HOTEL, VET, TEL_VET, CUIDADOS_ESPECIAIS, RACA, TEL_TUTOR, ATIVO)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ''', dados)
            self.conn.commit()
            return True
        except Exception as err:
            print(err)
            return False

    def deletar(self, iddenti):
        pass

    def caes_ativos(self):
        caes_ativos = self.c.execute('''
        select * from inscricoes where (ativo = 1)
        ''').fetchall()
        return caes_ativos

    def insert_into_ativos(self, jdados):
        """
        "cliente": resposta_form[5],
        "dias_por_semana": dias_por_semana,
        "valor_a_receber": valor_a_receber,
        "dia_de_pagamento": 5,
        "ativo":1,
        "tutor": "Cassio"
        :param jdados:
        :return:
        """
        try:
            valores = jdados['cliente'], jdados['dias_por_semana'], jdados['valor_a_receber'], jdados['dia_de_pagamento'], jdados['ativo'], jdados['tutor']
            # print(valores)
            _made = self.c.execute('''
            INSERT INTO ativos (Cliente, 'dias por semana', 'Valor a receber', 'Dia de pagamento', Ativo, Tutor)
            VALUES(?,?,?,?,?,?)
            ''', valores)

            self.conn.commit()
            return True
        except Exception as err:
            print(err)
            return False
        finally:
            self.conn.close()

    @staticmethod
    def get_remarks(nomecao):
        q = """
        SELECT diretrizes from inscricoes where(Dog like ?)
        """
        with ConectDb() as conn:
            res = conn.c.execute(q, [nomecao,]).fetchone()
        return res


class FaturasHotel(ConectDb):
    def __init__(self):
        super().__enter__()

        self.c.execute("""
                CREATE TABLE IF NOT EXISTS faturas_hotel(
                _ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NOME_CAO TEXT,
                TUTOR TEXT,
                EMAIL TEXT,
                DATA_ENTRADA TEXT,
                DATA_SAIDA TEXT,
                FATURA TEXT
                UNIQUE(TUTOR, NOME_CAO, DATA_ENTRADA, DATA_SAIDA)
                )
                """)


class Pagamentos(ConectDb):
    def __init__(self):
        super().__enter__()
        # self.conn = sqlite3.connect("dados/administracao.db")
        # self.c = self.conn.cursor()

        tabela_pagamentos = """
        CREATE TABLE IF NOT EXISTS pagamentos(
        _ID INTEGER PRIMARY KEY AUTOINCREMENT,
        NOME_TUTOR TEXT,
        NOME_CAO TEXT,
        VALOR TEXT,
        DATA_PAGAMENTO TEXT
        )
        """

        self.c.execute(tabela_pagamentos)
        self.conn.commit()

    def inserir_pagamento(self, tutor, cao, valor, data_pagamento):
        valores = tutor, cao, valor, data_pagamento
        inserir = """
        INSERT OR IGNORE INTO pagamentos(
        NOME_TUTOR, NOME_CAO, VALOR, DATA_PAGAMENTO
        ) VALUES(?,?,?,?)
        """
        self.c.execute(inserir, valores)
        self.conn.commit()

    def update(self, tutor, cao, valor, data_pagamento):
        dados = valor, data_pagamento, tutor, cao
        atualizar = """
        UPDATE pagamentos SET (VALOR, DATA_PAGAMENTO) = (?, ?) WHERE(NOME_TUTOR = ? AND NOME_CAO = ?)
        """
        try:
            self.c.execute(atualizar, dados)
        except Exception as err:
            print(err)
        finally:
            self.conn.commit()

    def check(self):
        retrieve = """
        SELECT * FROM pagamentos
        """
        return self.c.execute(retrieve).fetchall()

    def delete_entry(self, nome, cao, valor, data):
        valores = nome, cao, valor, data
        req_del = """
        DELETE FROM pagamentos WHERE(NOME_TUTOR = ? AND NOME_CAO = ? AND VALOR = ? AND DATA_PAGAMENTO = ?)
        """
        self.c.execute(req_del, valores)
        self.conn.commit()


class PresencasDB(ConectDb):
    def __init__(self):
        super().__enter__()
        # self.conn = sqlite3.connect("dados/administracao.db")
        # self.c = self.conn.cursor()
        self.c.execute("""
               CREATE TABLE IF NOT EXISTS presencas(
               _ID INTEGER PRIMARY KEY AUTOINCREMENT,
               DATA TEXT,
               TIPO TEXT,
               NOMECAO TEXT,
               public_id TEXT
               )
               """)
        self.conn.commit()

    def insert_presencas(self, data, tipo, nome, public_id=None, sent_by=None):
        try:
            dados = data, tipo, nome, public_id, sent_by
            q = """
            INSERT INTO presencas(DATA, TIPO, NOMECAO, public_id, usuario) VALUES(?,?,?,?,?)
            """
            self.c.execute(q, dados)
            self.conn.commit()
            return True
        except Exception as err:
            print(f"Um erro acontreceu no database handler linha 586{err}")
            return False

    def getpresencas(self):
        q = """
        SELECT * FROM presencas
        """
        return self.c.execute(q).fetchall()

    def delete_presencas(self, index):
        del_q = """
        DELETE FROM presencas WHERE(_ID = ?)
        """
        self.c.execute(del_q, [index,])
        self.conn.commit()


class FaturasDB(ConectDb):
    def __init__(self, **kwargs):
        try:
            self.mes = kwargs['mes']
            self.ano = kwargs['ano']
        except KeyError:
            try:
                with different_locale("pt_BR.utf-8"):
                    self.mes = calendar.month_abbr[datetime.now().month]
                    self.ano = datetime.now().year
                    self.nametabela = f"{self.mes}{self.ano}"
            except ValueError:
                print(f'[FROM DATABASEHANDLER] ValueError. Setando o nome da tabela estaticamente')
                self.nametabela = 'fev2022'


        super().__enter__()
        # create = f"""
        # CREATE TABLE IF NOT EXISTS {self.nametabela}(
        # _ID INTEGER PRIMARY KEY AUTOINCREMENT,
        # TIMESTAMP REAL,
        # NOMECAO TEXT,
        # TUTOR TEXT,
        # TELEFONE TEXT,
        # FATURA TEXT,
        # WLINK TEXT,
        # TOKEN TEXT UNIQUE
        # )"""
        # self.c.execute(create)
        # self.conn.commit()

    def get_banhos(self):
        pass

    def get_diarias(self):
        pass

    def set_get_valor_total(self):
        registrados = self.c.execute(f"SELECT TOKEN FROM {self.nametabela}").fetchall()
        ids = self.c.execute(f"SELECT dog FROM {self.nametabela}").fetchall()
        dados = dict()
        for eid in ids:
            token = uuid.uuid4().hex
            while token in registrados:
                token = uuid.uuid4().hex
            dados[token] = eid[0]
        itens = list(dados.items())
        print(itens)
        self.c.executemany(F"""
        UPDATE {self.nametabela} SET TOKEN=? WHERE Dog=?
        """, itens)
        self.conn.commit()

    def insert_data(self, nomecao, tutor, fatura, wlink, telefone):
        tokens = self.c.execute(f"SELECT TOKEN FROM {self.nametabela}").fetchall()
        token = uuid.uuid4().hex
        try:
            for token_registrado in tokens[0]:
                while token == token_registrado:
                    token = uuid.uuid4().hex
        except Exception as Err:
            print(Err)
        tscriacao = datetime.now().timestamp()
        data = tscriacao, nomecao, tutor, fatura, token, wlink, telefone
        q = """ 
        INSERT INTO faturas(TIMESTAMP, NOMECAO, TUTOR, FATURA, TOKEN, WLINK, TELEFONE) VALUES(?,?,?,?,?,?,?)
        """
        self.c.execute(q, data)
        self.conn.commit()
        faturas = {nomecao: token}
        print(faturas)
        return {nomecao: token}

    def get_fatura(self, token):
        q = f"""
        SELECT 
        Tutor, 
        dog,
        valor_creche,
        dias_hotel,
        databanho,
        quantidadebanhos,
        valorconsumo,
        total 
        FROM {self.nametabela} WHERE(TOKEN=?)
        """
        res = self.c.execute(q, [token,]).fetchone()
        print(f'[from databasehandler] res = {res}')
        return res

    def get_valor_total(self, token):
        q = F"""
        SELECT total FROM {self.nametabela} WHERE TOKEN=?
        """
        res = self.c.execute(q, [token,]).fetchone()
        return res

    def get_w_links(self):
        q = f"""
        SELECT Dog, TOKEN from {self.nametabela};
        """
        res = self.c.execute(q).fetchall()
        return res

    def update_total(self):
        q = f"""
        SELECT Dog, public_id, token, valor_creche, dias_hotel, 
        valorconsumo  
        from {self.nametabela}"""
        con = sqlite3.connect('dados/administracao.db')
        con.row_factory = sqlite3.Row
        c = con.cursor()
        c.execute(q)
        tokentotal = list()
        for e in c:
            lista = [0 if each == None else each for each in e[3:]]
            lista[1] *= 60
            tokentotal.append((e['token'], sum(lista)))
            # total = e["valor_creche"]  # +e['dias_hotel']*50+e['quantidadebanhos']*40,+e['valorconsumo']
            # print(total)
        for e in tokentotal:

            c.execute(F'UPDATE {self.nametabela} SET total=? WHERE TOKEN=?', [e[1], e[0]])
        con.commit()

class HorastrabalhadasDB(ConectDb):
    def __init__(self):
        super().__enter__()
        # self.conn = sqlite3.connect("dados/administracao.db")
        # self.c = self.conn.cursor()
        create_table = """
        CREATE TABLE IF NOT EXISTS horas_trabalhadas(
        _ID INTEGER PRIMARY KEY AUTOINCREMENT,
        TIMESTAMP REAL,
        NOME_PRESTADOR TEXT,
        PLANTOES24 INTEGER,
        DIAS24 TEXT,
        PLANTOES12 INTEGER,
        DIAS12 TEXT,
        PLANTOESFDS INTEGER,
        DIASFDS TEXT,
        ENTRADA TEXT,
        SAIDA TEXT 
        )
        """
        self.c.execute(create_table)
        self.conn.commit()

    def registrar_horas(self, formulario):
        timestamp = datetime.timestamp(datetime.now())
        dados = [dado for dado in formulario.values()]
        dados.insert(0, timestamp)
        insert_string = """
        INSERT OR IGNORE INTO horas_trabalhadas(TIMESTAMP,
        NOME_PRESTADOR, PLANTOES24, DIAS24, PLANTOES12, DIAS12, PLANTOESFDS, DIASFDS,ENTRADA,
        SAIDA
        ) VALUES (?,?,?,?,?,?,?,?,?,?)
        """
        self.c.execute(insert_string, dados)
        self.conn.commit()
        return True


if __name__ == '__main__':

    with FaturasDB() as fat:
        fat.update_total()
        # res = fat.get_fatura("a6e1400783904b818326f8932a3e7124")
        res = print(fat.get_valor_total("a6e1400783904b818326f8932a3e7124"))
        # print(fat.get_w_links())

        # print(res)
        # fat.set_token()

    # with Chegadas() as arr:
    #     print(arr.check_arrivals())

    # with ClockRecorder() as db:
    #     print(db.prestador_state('cassiorodrigo@gmail.com'))

        # print(db.is_clocked_in('cassiorodrigo@gmail.com'))
        # print(db.is_clocked_out('cassiorodrigo@gmail.com'))
        # db.insert_clockin('cassiorodrigo', "cassiorodrigo@gmail.com")
        # db.insert_clockin('cassio', "digo@gmail.com")
        # lin = db.is_clocked_in('cassiorodrigo@gmail.com')

        # print(lin)
    # with DatabaseCaes() as db:
    #     dogs = db.get_caes()
    #     print(dogs)
    # dbcaes = DatabaseCaes()
    # res = dbcaes.get_one_dog('beladsobrosa@hotmail.com')
    # print(res)
#     print(dbcaes.get_caes())
    # db_serv = DatabaseUsuarios()
    # db_serv.login_usuarios("cassiorodrigo", "Digo1660!")
    # pres = PresencasDB()
    # pres.insert_presencas("20-01-2022", "hotel", "Testes")
    # res = pres.getpresencas()
    # print(res)
    # pres.delete_presencas(1)
    # res = pres.getpresencas()
    # print(res)
    # chegadas = Chegadas()
    # arr = chegadas.check_arrivals()
    # print(arr)
    # banhos = Banhos()
    # banhos.inserir_banho('Testes', '25-01-2022', '02-02-2022', 'Médio')
    # banhos.inserir_banho('Testes', '28-01-2022', '02-01-2022', 'Médio')
    # print(banhos.mostrar_banhos())
    # pagamento = Pagamentos()
    # pagamento.inserir_pagamento('Testes', 'Cassio', '650', 'Hoje')
    # pagamento.update('Testes', 'Cassio', '600', 'Amanha')
    # pagamento.delete_entry('Testes', 'Cassio', '600', 'Amanha')
    # print(pagamento.check())
    # Chegadas().delete_arrival('Cassio', '23-01-2022')
    # novadata = DatabaseUsuarios()
    # _reg = novadata.registrar_usuario('Cassio', 'digo', 'cassiorodrigo@gmail.com', 'Digo1660!')
    # resultado = novadata.login_usuarios("digo", 'azul2')
    # _trocasenha = novadata.atualizar_senha(1, 'cassiorodrigo@gmail.com', 'azul2')
    # tudo = novadata.c.execute('''select * from login''').fetchall()
