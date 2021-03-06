# from flask_login import UserMixin
from flask_user import UserManager, UserMixin
from flask_wtf import FlaskForm
from wtforms import Form, StringField, EmailField,\
    PasswordField, SubmitField, BooleanField, DateField, TextAreaField, RadioField, TimeField, fields
from wtforms.validators import Email, EqualTo, Length, InputRequired
from wtforms_components import SelectField

from databasehandler import DatabaseUsuarios, ConectDb, DatabaseCaes


def getuser(id):
    with ConectDb() as db:
        res = db.c.execute("SELECT * FROM usuarios WHERE(PUBLIC_ID = ?)", [id,]).fetchone()
        return User(res[1], res[3], res[4], res[2], res[5], res[6])


class User(UserMixin):

    def __init__(self, public_id, name, email, username, role, dog):
        self.name = name
        self.email = email
        self.username = username
        self.role = 'cliente'
        self.public_id = public_id
        self.clockin = False
        self.clockout = False
        self.role = role
        self.dog = dog
        # with DatabaseCaes() as dbc:
        #     dog = dbc.get_one_dog(public_id)
        #     self.nomecao = dog

    def get_id(self):
        return self.public_id

    @staticmethod
    def login(user, pwd):
        db_servicos = DatabaseUsuarios()
        resultado = db_servicos.login_usuarios(user, pwd)
        email = db_servicos.email
        dog = db_servicos.dog
        name = db_servicos.nome
        username = db_servicos.username
        role = db_servicos.role
        public_id = db_servicos.public_id
        return User(public_id, name, email, username, role, dog)

    @staticmethod
    def registrar(username, nome, nomecao, email, pwd):
        db_servicos = DatabaseUsuarios()
        res = db_servicos.registrar_usuario(nome=nome, nomecao=nomecao, email=email, senha=pwd, usuario=username)  # nome, nomecao, usuario, email, senha
        return res


class Registrar(FlaskForm):
    # def registrar_usuario(self):
    nome = StringField(validators=[Length(min=5)], render_kw={"placeholder": "Nome"})
    usuario = StringField(validators=[Length(min=5)], render_kw={"placeholder": "Usuario"})
    cao = StringField(validators=[Length(min=5)], render_kw={"placeholder": "Nome do C??o"})
    email = EmailField(validators=[Email()], render_kw={"placeholder": "Email"})
    senha = PasswordField(validators=[Length(min=8)], render_kw={"placeholder": "Senha"})
    confirma_senha = PasswordField(validators=[Length(min=8)], render_kw={"placeholder": "Confirme a senha"})
    submit = SubmitField("Registrar")


class Logar(FlaskForm):
    nome = StringField(validators=[Length(min=5)], render_kw={"placeholder": "Nome"})
    usuario = StringField(validators=[Length(min=5)], render_kw={"placeholder": "Usuario"})
    email = EmailField(validators=[Email()], render_kw={"placeholder": "Email"})
    senha = PasswordField(validators=[Length(min=8)], render_kw={"placeholder": "Senha"})
    lembrar = BooleanField('Lembrar')
    submit = SubmitField("Logar")


class Adaptacao(FlaskForm):
    # def registrar_usuario(self):
    nome = StringField(validators=[Length(min=5)], render_kw={"placeholder": "Nome Tutor"})
    dog = StringField(validators=[Length(min=3)], render_kw={"placeholder": "Nome Cao"})
    raca = StringField(validators=[Length(min=5)], render_kw={"placeholder": "Ra??a"})
    email = EmailField(validators=[Email()], render_kw={"placeholder": "Email"})
    telefone = StringField(validators=[Length(min=10, max=12, message='Telefone com DDD')],
                           render_kw={"placeholder":"Telefone ex.: 27999999999"})
    diretrizes = TextAreaField(render_kw={"placeholder": "Orienta????es para estadia"})
    vacinado = BooleanField(label='Vacinado')
    vermifugado = BooleanField(label='Vermifugado')
    castrado = BooleanField(label='Castrado')
    crechehotel = RadioField(label='Adapta????o para crehce ou hotel?', choices=["Creche", 'Hotel'])
    date = DateField()
    submit = SubmitField("Enviar")


class Inscricao(Form):
    nome = StringField(validators=[Length(min=5), InputRequired()], render_kw={"placeholder": "Nome Tutor*"}, label='')
    dog = StringField(validators=[Length(min=3), InputRequired()], render_kw={"placeholder": "Nome Cao*"}, label='')
    raca = StringField(validators=[Length(min=5), InputRequired()], render_kw={"placeholder": "Ra??a*"}, label='')
    email = EmailField(validators=[Email(), InputRequired()], render_kw={"placeholder": "Email*"}, label='')
    telefone = fields.TelField(validators=[Length(min=10, max=12, message='Telefone com DDD'), InputRequired()],
                           render_kw={"placeholder": "Telefone ex.: 27999999999*"}, label='')
    endereco = StringField(validators=[Length(min=7, max=150)], render_kw={'placeholder': "Endere??o"}, label='')
    diretrizes = TextAreaField(render_kw={"placeholder": "Orienta????es para estadia"}, label='')
    vacinado = BooleanField(label='Vacinado', render_kw={"onchange":"checkall_to_activate_send()"})
    vermifugado = BooleanField(label='Vermifugado', render_kw={"onchange":"checkall_to_activate_send()"})
    castrado = BooleanField(label='Castrado', render_kw={"onchange":"checkall_to_activate_send()"})
    crechehotel = RadioField(validators=[InputRequired()], label='Inscricao para crehce ou hotel?*',
                             choices=["Creche", 'Hotel', 'Day Care'],
                             render_kw={"onchange": "escolhecreche()"})
    dataadaptacao = DateField(label='Dia da adapta????o')
    checkin = DateField(label='Data do Check-in')
    checkout = DateField(label='Data do Check-out')
    dias_por_semana = SelectField(label="",
                                 choices=[(1, '1 dia por semana'),
                                          (2, '2 dias por semana'),
                                          (3, '3 dias por semana'),
                                          (4, '4 dias por semana'),
                                          (5, '5 dias por semana'),
                                          (6, '6 dias por semana')])

    meio_periodo = RadioField(label='Per??odo', choices=[("1", "Meio Per??odo"), ("0", "Per??odo Integral")])
    nascimento_cao = DateField(label="Data de nascimento do c??o (aproximada se n??o souber)")
    historico_agressividade = TextAreaField(render_kw={"placeholder":'Descreva cuidados necess??rios com agressividade contra humanos ou outros c??es'}, label='')
    clinicavet = StringField(render_kw={'placeholder': 'Em caso de emerg??ncia, qual a cl??nica veterin??ria deveremos contactar?'}, label='')
    telclinicavet = fields.TelField(render_kw={'placeholder':'Qual o telefone da cl??nica veterin??ria?'}, label='')

    submit = SubmitField("Enviar", render_kw={"style": "width:50%; margin-bottom:60px", "class": "btn btn-info", "disabled":"disabled"})


class Banho(FlaskForm):
    nome = StringField(validators=[Length(min=3, max=20), InputRequired()], render_kw={'placeholder':'Nome do Tutor'})
    nome_cao = StringField(validators=[Length(min=3, max=20), InputRequired()], render_kw={'placeholder':'Nome do C??o'})
    databanho = DateField(label='Data do banho', validators=[InputRequired()])
    busca = TimeField(label='Hora que vai buscar: ', validators=[InputRequired()])
    perfume = BooleanField(label='Usar Perfume?')
    orientacoes = TextAreaField(label='Orienta????es ou cuidados especias: ',
                                render_kw={"placeholder": "Descreva se ?? necessario algum cuidado especial"
                                                          "durante o banho"})
    submit = SubmitField(label='Pedir Banho!')