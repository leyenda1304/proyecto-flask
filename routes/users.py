from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    session
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from extensions import db

from models.user import User

from forms.user_form import (
    RegistrationForm,
    LoginForm,
    EditProfileForm
)


users_bp = Blueprint('users', __name__)


# ==========================================
# INICIO - LISTA DE USUARIOS
# ==========================================

@users_bp.route('/')
def index():

    users = User.query.all()

    return render_template(
        'user_list.html',
        users=users
    )


# ==========================================
# REGISTRO
# ==========================================

@users_bp.route('/register', methods=['GET', 'POST'])
def register():

    form = RegistrationForm()

    if form.validate_on_submit():

        existing_user = User.query.filter(
            (User.username == form.username.data) |
            (User.email == form.email.data)
        ).first()

        if existing_user:

            flash(
                'El usuario o correo ya está registrado.',
                'error'
            )

            return render_template(
                'register.html',
                form=form
            )

        password_hash = generate_password_hash(
            form.password.data
        )

        user = User(
            username=form.username.data,
            email=form.email.data,
            password=password_hash
        )

        db.session.add(user)
        db.session.commit()

        flash(
            'Usuario registrado correctamente.',
            'success'
        )

        return redirect(
            url_for('users.login')
        )

    return render_template(
        'register.html',
        form=form
    )


# ==========================================
# LOGIN
# ==========================================

@users_bp.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(
            email=form.email.data
        ).first()

        if user and check_password_hash(
            user.password,
            form.password.data
        ):

            session['user_id'] = user.id
            session['username'] = user.username

            flash(
                'Inicio de sesión correcto.',
                'success'
            )

            return redirect(
                url_for(
                    'users.profile',
                    id=user.id
                )
            )

        flash(
            'Correo o contraseña incorrectos.',
            'error'
        )

    return render_template(
        'login.html',
        form=form
    )


# ==========================================
# CERRAR SESIÓN
# ==========================================

@users_bp.route('/logout')
def logout():

    session.clear()

    flash(
        'Sesión cerrada correctamente.',
        'success'
    )

    return redirect(
        url_for('users.index')
    )


# ==========================================
# PERFIL
# ==========================================

@users_bp.route('/profile/<int:id>')
def profile(id):

    user = User.query.get_or_404(id)

    return render_template(
        'profile.html',
        user=user
    )


# ==========================================
# EDITAR PERFIL
# ==========================================

@users_bp.route(
    '/profile/<int:id>/edit',
    methods=['GET', 'POST']
)
def edit_profile(id):

    user = User.query.get_or_404(id)

    form = EditProfileForm(
        obj=user
    )

    if form.validate_on_submit():

        # Comprobar si otro usuario utiliza
        # el mismo nombre o correo
        existing_user = User.query.filter(
            (
                (User.username == form.username.data) |
                (User.email == form.email.data)
            ) &
            (User.id != user.id)
        ).first()

        if existing_user:

            flash(
                'El nombre de usuario o correo ya está utilizado.',
                'error'
            )

            return render_template(
                'edit_profile.html',
                user=user,
                form=form
            )

        user.username = form.username.data
        user.email = form.email.data

        db.session.commit()

        # Actualizar nombre de usuario en la sesión
        if session.get('user_id') == user.id:

            session['username'] = user.username

        flash(
            'Perfil actualizado correctamente.',
            'success'
        )

        return redirect(
            url_for(
                'users.profile',
                id=user.id
            )
        )

    return render_template(
        'edit_profile.html',
        user=user,
        form=form
    )


# ==========================================
# ELIMINAR PERFIL
# ==========================================

@users_bp.route(
    '/profile/<int:id>/delete',
    methods=['POST']
)
def delete_profile(id):

    user = User.query.get_or_404(id)

    db.session.delete(user)

    db.session.commit()

    if session.get('user_id') == id:

        session.clear()

    flash(
        'Usuario eliminado correctamente.',
        'success'
    )

    return redirect(
        url_for('users.index')
    )