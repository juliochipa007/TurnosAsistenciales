from flask import Flask
from flask_mysqldb import MySQL
from routes.auth import auth_bp
from routes.login import login_bp
from routes.crearuser import crearuser_bp
from routes.principal import principal_bp

app = Flask(__name__, template_folder='templates')

# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # Cambia esto si tu contraseña no está vacía
app.config['MYSQL_DB'] = 'turnosasis'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

# Configuración de seguridad de la sesión
app.secret_key = "clave_secreta_segura"
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False  # Cambia a True en producción (HTTPS)
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Registrar blueprints
app.register_blueprint(login_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(crearuser_bp)
app.register_blueprint(principal_bp)

if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=4500, use_reloader=True)