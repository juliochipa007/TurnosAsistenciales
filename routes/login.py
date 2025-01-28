# routes/login.py
from flask import Blueprint, render_template, request, redirect, session
from werkzeug.security import check_password_hash
from flask_mysqldb import MySQL

mysql = MySQL()

login_bp = Blueprint('login', __name__, template_folder='templates')

# Ruta para el login (destruye la sesión actual)
@login_bp.route("/")
def login():
    session.clear()  # Destruye todas las sesiones activas
    return render_template("login.html")

# Ruta para cerrar sesión
@login_bp.route("/logout")
def logout():
    session.clear()  # Destruye todas las sesiones activas
    return redirect("/")
