import json, time, flask, sqlite3, os, requests
from geradorpix import QRPix
from flask import Flask, request, jsonify, Response, render_template, redirect, url_for, make_response, session
from flask_restful import Resource, Api
from datetime import datetime, timedelta, timezone, date
from databasehandler import DatabaseUsuarios, DatabaseCaes, Chegadas, Banhos, Pagamentos, PresencasDB,\
    FaturasDB, HorastrabalhadasDB, ClockRecorder
from tratadadosinscricao import InscreverDog
from flask_login import login_user, login_required, LoginManager, current_user, logout_user
from edit_tables import Connection
from flask_bootstrap import Bootstrap
from authflask import Registrar, Logar, User, getuser, Adaptacao, Inscricao, Banho
from telegramsender import FormSent, PedidoBanhos
import base64

CHAVE = os.getenv("chaveapi")
app = Flask(__name__)
app.secret_key = CHAVE
api = Api(app)
bstrap = Bootstrap(app)
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
app.config['JSON_AS_ASCII'] = False
usuario = None
token = None
flashclass = "alert-dismissible fade show"


@login_manager.user_loader
def load_user(user_id):
    usuario = getuser(user_id)
    return usuario


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("login"))


class Tabelas(Resource):
    def get(self):
        argumentos = request.args.to_dict()
        with Connection() as conn:
            if ['tabela', 'coluna', 'filtro'] == list(argumentos.keys()):
                dados = {
                    'headers': conn.c.execute(f'PRAGMA table_info({argumentos.get("tabela")})').fetchall(),
                    'dados': conn.c.execute(f'''select {argumentos.get('coluna')} 
                    from {argumentos.get('tabela')}''').fetchall()
                }

                return jsonify(dados)

            elif ['tabela', 'coluna'] == list(argumentos.keys()):
                return conn.c.execute(f'select {argumentos.get("coluna")} from {argumentos.get("tabela")}').fetchall()

            if 'tabela' in argumentos.keys():
                return jsonify(conn.c.execute(f'PRAGMA table_info({argumentos.get("tabela")})').fetchall())

    def post(self, *args, **kwargs):
        valores = [value for value in request.args.values()]
        with Connection() as conn:
            colunas = conn.get_table_columns(valores[0])
            print(f'[main linha 64] {colunas}')
            pega = conn.c.execute(f'SELECT * FROM {valores[0]}').fetchall()
        return make_response(jsonify(pega))


api.add_resource(Tabelas, "/edit")


@app.route('/inscricao', methods=["GET", "POST"])
def inscricao():

    if request.method == "GET":
        form = Inscricao()
        return render_template('inscricoes.html', form=form)
    else:
        formulario = request.form.to_dict()
        print(f"")
        newdog = InscreverDog(**formulario).inscrever_dog()
        flask.flash(f"Mensagem recebida. Trocar mensagem")
        return redirect(url_for("welcome"))

def get_values(*args, **kwargs):
    print(kwargs)
    print(args)

@app.route("/edit_table", methods=["GET", "POST"])
def edit_table(*args, **kwargs):
    if request.method == 'GET':
        with Connection() as conn:
            tabelas = conn.get_nome_tabelas()
        return render_template('edit_databases.html', tabelas=tabelas)
    else:
        valores = list(request.form.listvalues())
        print(valores+"from edit table in line 99")
        return redirect(url_for('edit_table', valores=valores))


@app.get("/links")
def links():
    flask.flash("Você não deveria ver essa página", f"alert alert-info alert-dismissible show")
    return render_template("links.html")


def string_fat(token):
    with FaturasDB() as fat:
        res = fat.get_fatura(token)
        with open('templatetextos/basefaturas.txt', 'r', encoding='UTF-8') as file:
            reader = file.read()
            return reader.format(*res)


@app.route('/fatura', methods=["GET", "POST"])
def fatura():
    if request.method == 'GET':
        with FaturasDB() as fdb:
            try:
                faturas_token = request.args.get('token')
                token_existe = True
            except TypeError as terror:
                token_existe = False
                print('não achou o token')
                print(terror)
            if faturas_token is not None:
                try:
                    print(f'[FROM FATURA LINHA 137] print token {faturas_token}')
                    result = string_fat(faturas_token)
                    valor = fdb.get_valor_total(faturas_token)[0]


                except TypeError as terror2:
                    flask.flash(str(terror2), f"alert alert-info {flashclass}")
                    result = ''
                    valor = 1
                get_all_links = ''
            else:
                get_all_links = fdb.get_w_links()
                result = ''
                valor = 1

        chave_pix = "11c358f9-a42d-434f-b791-f176de78f215"

        qrpix = bytes(QRPix(chave_pix, float(f"{valor:.2f}"), 'CASSIO RODRIGO D ANTONIO ', 'SAO PAULO', "05409000", 'Asercolocadodepois'))
        copiaecola = QRPix(chave_pix, float(f"{valor:.2f}"), 'CASSIO RODRIGO D ANTONIO ', 'SAO PAULO', "05409000", 'Asercolocadodepois').salvar_qrcode()
        res = base64.b64encode(qrpix)

        return render_template('fatura.html', dog_fat=result, links=get_all_links, imagem=res.decode('UTF-8'),
                               chave_pix=chave_pix,
                               copiaecola=copiaecola)
    else:
        faturas = request.json
        with FaturasDB() as nfat:
            for k, v in faturas.items():
                print(k)
                v = json.loads(v)
                nfat.insert_data(v['nomecao'], v['tutor'], v['fatura'], v['whatsapp'], v['telefone'])
            flask.flash("Dados recebidos com sucesso", f"alert-info {flashclass}")
        return redirect(url_for('home'))


@app.route("/registrar", methods=["GET", "POST"])
def registrar():
    form = Registrar()
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    if request.method == "GET":
        return render_template("register.html", form=form)
    else:
        if form.validate_on_submit():
            data = form.data
            new_user = User.registrar(username=data["usuario"], nomecao=data["cao"], nome=data["nome"], email=data["email"], pwd=data['senha'])
            if new_user:
                flask.flash("Usuario criado com sucesso. Por favor, faça o Login.", f"alert aflert-info {flashclass}")
                return redirect(url_for('login'))
            else:
                flask.flash("Algo errado não está certo", f"alert alert-danger {flashclass}")
                flask.flash(f"{DatabaseUsuarios.err}",
                            f"alert alefrt-danger fade show {flashclass}")
                return render_template("register.html", form=form)

        else:
            flask.flash(f"Algo errado não está certo", f"alert alefrt-danger fade show {flashclass}")
            return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    global usuario
    global token
    form = Logar()
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    if request.method == "GET":
        return render_template("login.html", form=form)
    elif request.method == "POST":
        try:
            usuario = User.login(form.usuario.data, form.senha.data)
            logged = usuario.login(form.usuario.data, form.senha.data)
            if logged:
                _user_logged = login_user(usuario, form.lembrar.data)
                flask.flash("Logado com Sucesso", f"alert alert-info {flashclass}")
                return redirect(url_for('perfil', username=current_user.username))
            else:
                flask.flash("Login falhou. Você digitou usuario e senha corretos?", f"alert alert-danger {flashclass}")
                return redirect(url_for('login'))
        except TypeError as Terror:
            flask.flash(f"Login falhou: {Terror}", f"alert alert-danger {flashclass}")
            return redirect(url_for('login'))


@app.route("/", methods=["GET"])
def welcome():
    if current_user.is_authenticated:
        return redirect(url_for('home',  usuario=current_user.username))

    return render_template('base.html')

@app.route("/<usuario>", methods=["GET"])
@login_required
def home(usuario):
    # flask.flash(f"Usuario: {current_user.name}", f"alert alert-danger {flashclass}")
    return render_template("base.html")


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route('/registrar_horas', methods=["GET", "POST"])
@login_required
def horastrabalhadas():
    if request.method == 'GET':
        if current_user.role != 'cliente':
            if request.host_url in request.referrer:
                return render_template("horas_trabalhadas.html")
    else:
        if request.host_url in request.referrer:
            if current_user.role != "cliente":
                formulario = request.form.to_dict()
                if HorastrabalhadasDB().registrar_horas(formulario):
                    flask.flash("Horas trabalhadas logadas com Sucesso", f"alert alert-info {flashclass}")
                    return render_template("horascadastradascomsucesso.html")
                else:
                    return flask.flash("Algo de errado não está certo. Avise o Cássio", f"alert alert-danger {flashclass}")
            return flask.flash("Algo de errado não está certo. Avise o Cássio", f"alert alert-danger {flashclass}")


@app.route('/frequencia', methods=["GET", "POST"])
@login_required
# @roles_required('superadmin')
def freq():
    if request.method == "GET":
        if current_user.role != 'cliente':
            with DatabaseCaes() as dbcaes:
                dogs = dbcaes.get_caes()
            return render_template("frequencia.html", dogs=dogs)
    else:
        valores = request.form.to_dict()
        print(valores)
        timestamp = valores.get('datetime')
        if timestamp == '':
            timestamp = datetime.timestamp(datetime.now())
        nomes_presencas = list(filter(lambda x: True if x != 'datetime' and x != 'crechehotel' else False, valores.keys()))
        for dog in nomes_presencas:
            with PresencasDB() as pre:
                pre.insert_presencas(
                    data=timestamp,
                    tipo=valores.get('crechehotel'),
                    nome=dog,
                    public_id=valores.get(dog),
                    sent_by=current_user.username
                )
        new_sender = FormSent(
            username=current_user.username,
            tipo=valores.get('crechehotel'),
            dogsin=nomes_presencas
        )
        new_sender.enviar_mensagem()


    flask.flash('Caes inseridos com sucesso! Muito Obrigado', f'alert-info {flashclass}')
    return redirect(url_for('welcome', username=current_user.username))


@app.route("/clockin", methods=["GET", "POST"])
def clockin():
    current_user.clockintime = None
    if request.method == "GET":
        if current_user.role != 'cliente':
            with ClockRecorder() as db:
                if db.prestador_state(current_user.email):
                    current_user.clockin = True
                    current_user.clockout = False
                    current_user.clockintime = db.get_clockin_time(current_user.email)
                    since = f"{time.localtime(current_user.clockintime[0]).tm_hour} : {time.localtime(current_user.clockintime[0]).tm_min} : {time.localtime(current_user.clockintime[0]).tm_sec}"
                    flask.flash(f"O usuario {current_user.name} está logado desde {since}",
                                f"alert alert-info {flashclass}")
                else:
                    current_user.clockin = False
                    current_user.clockout = True

            tz = timezone(timedelta(hours=-3))

            return render_template("clockin.html", current_user=current_user, datetime=datetime, tz=tz, time=time)
        else:
            return redirect(url_for('home'))
    else:
        with ClockRecorder() as db:
            db.insert_clockin(current_user.username, current_user.email)
            if db.prestador_state(current_user.email):
                current_user.clockin = True
                current_user.clockout = False
            else:
                current_user.clockin = False
                current_user.clockout = True
        return redirect(url_for('clockin'))


@app.route("/<string:username>", methods=["GET"])
def perfil(username):
    return render_template("paginapessoal.html", current_user=current_user)


@app.route('/formulariorecebido')
def formulario_recebido():
    flask.flash('Recebido!', f"alert-info {flashclass}")
    return render_template('formulariorecebido.html')

@app.route("/adaptacao", methods=["GET", "POST"])
def ficha_adaptacao():
    form = Adaptacao()
    if request.method == 'GET':
        return render_template('ficha_adaptacao.html', form=form)
    else:
        resposta = list(request.form.values())[1:-1]

        print(resposta)
        resposta.pop(5)
        resposta.pop(5)
        resposta.pop(5)
        print(resposta)
        with Chegadas() as chdb:
            chdb.insert_adaptacao(resposta=resposta)
        return redirect(url_for('formulario_recebido'))

@app.route("/clientes")
def mostra_clientes():
    return render_template("mostrar_clientes.html", current_user=current_user)


# @app.route("/<string:username>/fatura", methods=["GET"])
# def fatura(*args, **kwargs):
#     dados = DatabaseCaes()
#     try:
#         res = dados.get_one_dog(current_user.email)
#         if current_user.role == "superadmin":
#             res = dados.get_caes()
#     except Exception as err:
#         print(err)
#     finally:
#         dados.conn.close()
#     return render_template("fatura.html", current_user=current_user, dog=res)


class Hotel(Resource):
    def get(self):
        if request.host_url in request.referrer:
            conn = sqlite3.connect("dados/base_caes.db")
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("select * from inscricoes WHERE(DIAS_POR_SEMANA LIKE '%otel%'  OR DIAS_POR_SEMANA LIKE 'Day%')")
            resposta = [dict(row) for row in c.fetchall()]
            conn.close()
            resultado = list(filter(lambda x: datetime.strptime(x['SAIDA_HOTEL'], "%d/%m/%Y") >= datetime.now(), resposta))
            print(resultado)
            return jsonify(resultado)
        else:
            return Response("Acesso negado", 401)

    def post(self):
        if request.host_url in request.referrer:
            dados = request.json
            # data = monta_data()
            # dbinstance = DatabaseCaes()
            # dbinstance.inserir_presencas(data, "hotel", str(dados["hotel"]), str(dados["funcionario"]))
            return dados


class DayCare(Resource):
    def get(self):
        pass


class Creche(Resource):
    def get(self):
        if request.host_url in request.referrer and current_user.role == "admin":
            resposta = DatabaseCaes().get_caes()
            return jsonify(resposta)
        else:
            return Response("Acesso negado", 401)

    def post(self):
        if request.host_url in request.referrer:
            dados = json.loads(request.headers['payload'])
            # data = monta_data()
            novainstancia = DatabaseCaes()
            novainstancia.inserir_inscricoes(dados)


class ChegadasPrevistas(Resource):

    def post(self, nome, chegada, saida, adaptacao):
        Chegadas().insert_new_arrival(nome, chegada, saida, adaptacao)

    def delete(self, nome, chegada):
        if request.host_url in request.referrer:
            Chegadas().delete_arrival(nome, chegada)

    def get(self):
        try:
            if request.host_url in request.referrer:
                if current_user.role != 'cliente':
                    return Chegadas().check_arrivals()
        except Exception as err:
            flask.flash("Houve um erro", f"alert alert-danger {flashclass}")
            return redirect((url_for('welcome')))


    @staticmethod
    @app.route('/chegadasprevistas')
    @login_required
    def homechegadas():
        cuidados = dict()
        try:
            with Chegadas() as chd:
                nomes_chegadas = chd.get_arrivals_names()

            for nome in nomes_chegadas:
                try:
                    cuidados[nome[0]] = Diretrizes().get(nomecao=nome[0])
                    print(cuidados)
                except Exception as err:
                    print(err)
        except Exception as err:
            print(f"um erro aconteceu: {err}")

        if request.host_url in request.referrer and current_user.role != 'cliente':
            dia = datetime.now().day
            mes = datetime.now().month
            ano = datetime.now().year
            ts_hoje = datetime.timestamp(datetime(ano, mes, dia, 0, 10))
            ts_amanha = datetime.timestamp(datetime(ano, mes, dia, 23, 59))
            inout = ts_hoje, ts_amanha

            return render_template('chegadas.html', inout=inout, datetime=datetime, date=date, cuidados=cuidados)
        else:
            return redirect(url_for('home'))


class BanhosPedidos(Resource):
    def get(self):
        try:
            if request.host_url in request.referrer:
                res = Banhos().mostrar_banhos()
                return res
            else:
                return flask.flash("Token não confere. Acesso negado", f"alert alert-danger {flashclass}")
        except Exception as err:
            print(err)
            flask.flash(f"Um erro ocorreu: {err}", 'falert alert-warning {flashclass}')
            return redirect(url_for('home'))

    def post(self, nome, data_pedido, data_banho, tamanho):
        try:
            Banhos().inserir_banho(nome, data_pedido, data_banho, tamanho)
        except Exception:
            return 501

    def delete(self, nome, data):
        try:
            if request.host_url in request.referrer and current_user.role == "admin":
                Banhos().deletar_banho(nome, data)
        except Exception as err:
            print(err)
            return 509

    @staticmethod
    @app.route('/banhospedidos', methods=["GET", "POST"])
    @login_required
    def banhos_pedidos():
        if request.method == "GET":
            if current_user.role != "cliente":
                return render_template('banhospedidos.html', userinfo=current_user)
            else:
                flask.flash("Voce não tem permissão para ver essa página", "falert alert-warning {flashclass}")
                return redirect(url_for("home"))
        else:
            try:
                res = request.form.to_dict()
                for k, v in res.items():
                    splited = k.split(", ")
                    print(f'Splited nos banhos: 0: {splited[0]}, 1: {splited[2]}, value: {v}')
                    Banhos().update_banho_tomado(splited[0], splited[2], bool(v))
                mensagem = """
                Os Banhos dados foram enviados com sucesso!
                
                Muito Obrigado!
                """
                flask.flash(mensagem, f'alert alert-info {flashclass}')
                return redirect(url_for('banhos_pedidos'))
            except Exception as err:
                mensagem = f"""
                Alguma coisa deu errado. 
                
                erro: {err}
                """
                flask.flash(mensagem, f'alert alert-danger {flashclass}')
                return redirect(url_for('banhos_pedidos'))

    @staticmethod
    @app.route('/pedirbanho', methods=['GET', "POST"])
    def pedirbanho():
        form = Banho()
        if request.method == 'GET':
            return  render_template("pedidobanho.html", form=form)

        else:
            print(request.form.to_dict())
            if current_user.is_authenticated:
                nome = current_user.name
                nomecao = current_user.nomecao
                flask.flash(f"{nome}: {nomecao}", flashclass)
                return redirect(url_for('home', usuario=current_user.username))
            else:
                return redirect(url_for('welcome'))

class PagamentosRegistrar(Resource):

    def get(self):
        if request.host_url in request.referrer:
            registrado = Pagamentos().check()
            return registrado

    def post(self, nome, cao, valor, data):
        if request.host_url in request.referrer:
            Pagamentos().inserir_pagamento(nome, cao, valor, data)

    def put(self, nome, cao, valor, data):
        if request.host_url in request.referrer:
            dados = request.form.to_dict()
            print(dados)
            # Pagamentos().update(nome, cao, valor, data)

    def delete(self, nome, cao, valor, data):
        if request.host_url in request.referrer:
            Pagamentos().delete_entry(nome, cao, valor, data)


class Presencas(Resource):
    def get(self):
        if request.host_url in request.referrer:
            return PresencasDB().getpresencas()

        else:
            return "Um erro aconteceu"

    def post(self):
        if request.host_url in request.referrer:
            listadelistas = request.json
            for lista in listadelistas:
                nomes = lista[2:]
                if len(nomes) > 0:
                    for dognames in nomes:
                        for dogname in dognames.split(","):
                            PresencasDB().insert_presencas(lista[0], lista[1], dogname)
        else:
            return "Um erro aconteceu"

    def delete(self, index):
        if request.host_url in request.referrer:
            return PresencasDB().delete_presencas(index)
        else:
            return "Houve uma falha"


class Diretrizes(Resource):

    def get(self, nomecao):
        with DatabaseCaes() as dbc:
            res = dbc.get_remarks(nomecao=nomecao)
            res = dbc.get_remarks(nomecao=nomecao)
        return res

api.add_resource(Presencas, f"/presencas/", "/presencas/<string:index>")
api.add_resource(Hotel, f'/hotel/')
api.add_resource(DayCare, f'/daycare/')
api.add_resource(Creche, f'/creche/',
                 f'/creche/<string:nome>')
api.add_resource(ChegadasPrevistas, f"/chegadas/",
                 f"/chegadas/<string:nome>/<string:chegada>/<string:saida>/<string:adaptacao>",
                 f"/chegadas/remove/<string:nome>/<string:chegada>")

api.add_resource(Diretrizes, f"/diretrizes/<string:nomecao>", endpoint='diretrizes')
api.add_resource(BanhosPedidos, f"/banhos",
                     f"/banhos/<string:nome>/<string:data_pedido>/<string:data_banho>/<string:tamanho>/0/<integer:perfume>/0.1/<string:orientacoes>",
                 f"/banhos/<string:nome>/<string:data>")

api.add_resource(PagamentosRegistrar, f"/pagamentos/",
                 f'/pagamentos/<string:nome>/<string:cao>/<string:valor>/<string:data>')

# api.add_resource(Faturas, f"/faturas",
#                  f"/faturas/<string:nomecao>/<string:nometutor>/<string:diasporsemana>/<string:diashotel>/<string:banhos>")

app.jinja_env.globals["getchegadas"] = ChegadasPrevistas().get
app.jinja_env.globals["getbanhos"] = BanhosPedidos().get
app.jinja_env.filters["get_values"] = get_values


if __name__ == "__main__":
    app.run(host='192.168.1.123', port=5000, debug=True)
