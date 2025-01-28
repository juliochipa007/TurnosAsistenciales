from flask import Blueprint, render_template, request, redirect, session, flash, jsonify
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from flask_mysqldb import MySQL

mysql = MySQL()

crearuser_bp = Blueprint('crearuser', __name__, template_folder='templates')

@crearuser_bp.route("/Crear-Usuario-nuevo")
def crearUser():
    session.clear()  # Destruye todas las sesiones activas
    return render_template("crearUser.html")

# Ruta para registrar nuevos usuarios (POST)
@crearuser_bp.route("/registrar-usuario", methods=["POST"])
def registrar_usuario():
    if request.method == "POST":
        # Recoger los datos del formulario
        _apellidos = request.form["ape_user"]
        _nombres = request.form["name_user"]
        _dni = request.form["dni_user"]
        _password = request.form["pass_user"]

        # Validaciones básicas
        if not _apellidos.strip() or not _nombres.strip():
            return jsonify({"error": "Los nombres y apellidos no deben estar vacíos."}), 400

        if not _dni.isdigit() or len(_dni) != 8:
            return jsonify({"error": "El DNI debe tener 8 dígitos y ser numérico."}), 400

        # Verificar si el DNI ya existe en la base de datos
        cur = mysql.connection.cursor()
        cur.execute("SELECT dni_user FROM users WHERE dni_user = %s", (_dni,))
        existe = cur.fetchone()
        cur.close()

        if existe:
            return jsonify({"error": "Este DNI ya esta registrado."}), 400

        # Cifrar la contraseña
        hashed_password = generate_password_hash(_password)

        # Guardar los datos en la base de datos
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO users (ape_user, name_user, dni_user, pass_user) 
            VALUES (%s, %s, %s, %s)
        """, (_apellidos.upper(), _nombres.upper(), _dni, hashed_password))
        mysql.connection.commit()
        cur.close()

        return render_template('crearUser.html', mensaje="Se registro usuario correctamente")

    return jsonify({"error": "Método no permitido."}), 405
