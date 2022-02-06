# from flask_login import UserMixin
from flask_user import UserManager, UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, ValidationError, IntegerField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Email, EqualTo, Length
from flask_bcrypt import generate_password_hash
from databasehandler import DatabaseUsuarios, ConectDb


def getuser(id):
    print(id)
    with ConectDb() as db:
        res = db.c.execute("SELECT * FROM usuarios WHERE(PUBLIC_ID = ?)", [id,]).fetchone()
        print(res)
        return User(res[1], res[3], res[4], res[2], res[5])


class User(UserMixin):

    def __init__(self, public_id, name, email, username, role):
        self.name = name
        self.email = email
        self.username = username
        self.role = 'cliente'
        self.public_id = public_id
        self.clockin = False
        self.clockout = False
        self.role = role

    def get_id(self):
        return self.public_id

    @staticmethod
    def login(user, pwd):
        db_servicos = DatabaseUsuarios()
        resultado = db_servicos.login_usuarios(user, pwd)
        email = db_servicos.email
        name = db_servicos.nome
        username = db_servicos.username
        role = db_servicos.role
        public_id = db_servicos.public_id
        return User(public_id, name, email, username, role)

    @staticmethod
    def registrar(username, nome, email, pwd):
        db_servicos = DatabaseUsuarios()
        res = db_servicos.registrar_usuario(nome, username, email, pwd)
        return res


class Registrar(FlaskForm):
    # def registrar_usuario(self):
    nome = StringField(validators=[Length(min=5)], render_kw={"placeholder": "Nome"})
    usuario = StringField(validators=[Length(min=5)], render_kw={"placeholder": "Usuario"})
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


# if __name__ == "__main__":
#     usuario = User().login("cassiorodrigo", "Digo1660!")
