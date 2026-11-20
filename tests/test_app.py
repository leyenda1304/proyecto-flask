
from app import app
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash


def test_app_se_crea_correctamente():
    assert app is not None
    assert app.name == "app"


def test_rutas_principales_existen():
    rutas = [rule.rule for rule in app.url_map.iter_rules()]

    assert "/" in rutas
    assert "/register" in rutas
    assert "/login" in rutas
    assert "/logout" in rutas


def test_modelo_usuario():
    usuario = User(
        username="usuario_prueba",
        email="prueba@example.com",
        password="hash_prueba"
    )

    assert usuario.username == "usuario_prueba"
    assert usuario.email == "prueba@example.com"
    assert usuario.password == "hash_prueba"


def test_generar_y_verificar_contrasena():
    contrasena = "Prueba123"
    password_hash = generate_password_hash(contrasena)

    assert check_password_hash(password_hash, contrasena)
    assert not check_password_hash(password_hash, "incorrecta")


def test_cerrar_sesion():
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False

    cliente = app.test_client()

    with cliente.session_transaction() as sesion:
        sesion["user_id"] = 1
        sesion["username"] = "usuario_prueba"

    respuesta = cliente.get("/logout", follow_redirects=False)

    assert respuesta.status_code == 302

    with cliente.session_transaction() as sesion:
        assert "user_id" not in sesion
        assert "username" not in sesion
