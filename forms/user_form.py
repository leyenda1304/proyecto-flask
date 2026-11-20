from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class RegistrationForm(FlaskForm):

    username = StringField(
        'Nombre de usuario',
        validators=[
            DataRequired(),
            Length(min=3, max=50)
        ]
    )

    email = StringField(
        'Correo electrónico',
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        'Contraseña',
        validators=[
            DataRequired(),
            Length(min=6, max=255)
        ]
    )

    confirm_password = PasswordField(
        'Confirmar contraseña',
        validators=[
            DataRequired(),
            EqualTo(
                'password',
                message='Las contraseñas deben coincidir.'
            )
        ]
    )

    submit = SubmitField('Registrarse')


class LoginForm(FlaskForm):

    email = StringField(
        'Correo electrónico',
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        'Contraseña',
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField('Iniciar sesión')


class EditProfileForm(FlaskForm):

    username = StringField(
        'Nombre de usuario',
        validators=[
            DataRequired(),
            Length(min=3, max=50)
        ]
    )

    email = StringField(
        'Correo electrónico',
        validators=[
            DataRequired(),
            Email()
        ]
    )

    submit = SubmitField('Guardar cambios')