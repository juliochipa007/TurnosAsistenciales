# routes/auth.py

from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from werkzeug.security import check_password_hash
from flask_mysqldb import MySQL

mysql = MySQL()

auth_bp = Blueprint('auth', __name__, template_folder='templates')

# Validación de login
@auth_bp.route("/validar-login", methods=["POST"])
def validar():
    if request.method == "POST":
        _usuario = request.form["txtUser"]
        _password = request.form["txtPassword"]

        # Buscar al usuario en la base de datos
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE dni_user=%s", (_usuario,))
        datosCuenta = cur.fetchone()
        cur.close()

        if datosCuenta:
            # Validar la contraseña
            hashed_password = datosCuenta["pass_user"]
            print(hashed_password)

            if check_password_hash(hashed_password, _password):
                # Iniciar sesión
                session["logueado"] = True
                session["id_user"] = datosCuenta["id_user"]
                session["name_user"] = datosCuenta["name_user"]
                session["dni_user"] = datosCuenta["dni_user"]
                    # Redirigir al dashboard ADMIN
                return redirect("/principal")

            else:
                # Pasar el mensaje de error al template
                return render_template("login.html", mensaje="Usuario o contraseña incorrectos")
        else:
            # Pasar el mensaje de error al template
            return render_template("login.html", mensaje="Usuario o contraseña incorrectos")
