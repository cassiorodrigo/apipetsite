import locale
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
from flask_sqlalchemy import SQLAlchemy
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